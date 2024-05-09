import mmap
import elf
import ctypes
import sys
import numpy as np
from pprint import pprint
from contextlib import closing

pagesize = mmap.PAGESIZE
print(mmap.ALLOCATIONGRANULARITY)

libc = ctypes.cdll.LoadLibrary(None)
lmmap = libc.mmap
lmmap.restype = ctypes.c_void_p
lmmap.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_size_t)

mprotect = libc.mprotect
mprotect.restype = ctypes.c_int
mprotect.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int)

mmap2 = libc.mmap
mmap2.restype = ctypes.c_void_p
mmap2.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_size_t)


malloc = libc.malloc
malloc.restype = ctypes.c_void_p
malloc.argtypes = (ctypes.c_size_t,)

# This doesn't work, the return is in rax and we need it xmm0
@ctypes.CFUNCTYPE(ctypes.c_uint16, ctypes.c_double)
def __truncdfhf2(x):
    return 3
    # return x

libs = {"__truncdfhf2": __truncdfhf2}

file = sys.argv[1]
with open(file) as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY)
    hdr = elf.Elf64_Ehdr.from_buffer(mm)
    sections = (elf.Elf64_Shdr*hdr.e_shnum).from_buffer(mm, hdr.e_shoff)
    shstroff = sections[hdr.e_shstrndx].sh_offset
    section_names = {ctypes.string_at(mm[shstroff + s.sh_name:]).decode('ascii'): i for i, s in enumerate(sections)}
    pprint(section_names)
    symtabhdr = sections[section_names['.symtab']]
    strtabhdr = sections[section_names['.strtab']]

    nsymbols = symtabhdr.sh_size // symtabhdr.sh_entsize
    symbolinfo = (elf.Elf64_Sym*nsymbols).from_buffer(mm, symtabhdr.sh_offset)

    symbols = {ctypes.string_at(mm[strtabhdr.sh_offset + s.st_name:]).decode('ascii'): i for i, s in enumerate(symbolinfo)}
    def load(name):
        section = sections[section_names[name]]
        if '.rela'+name not in section_names:
            return section
        relhdr = sections[section_names['.rela'+name]]
        nrel = relhdr.sh_size // relhdr.sh_entsize
        relocations = (elf.Elf64_Rela*nrel).from_buffer(mm, relhdr.sh_offset)
        relsections = []
        got = []
        for rel in relocations:
            sidx = rel.r_info >> 32
            ts = rel.r_info & 0xffffffff
            if ts == elf.R_X86_64_GOTPCRELX or ts == elf.R_X86_64_REX_GOTPCRELX:
                got.append(sidx)
            if symbolinfo[sidx].st_shndx not in relsections:
                relsections.append(symbolinfo[sidx].st_shndx)

        alignment = 64
        print(got)
        allocs = [[section_names[name]]]
        sum = section.sh_size
        for s in relsections:
            print(s, sum)
            if sum + sections[s].sh_size < pagesize:
                allocs[-1].append(s)
                sum += sections[s].sh_size
                sum = (sum + alignment - 1) & -alignment
            else:
                allocs.append([])
                allocs[-1].append(s)
                sum = (sections[s].sh_size + alignment -1) & -alignment

        r = mmap.mmap(-1, (len(allocs)+1)*pagesize, access=mmap.ACCESS_WRITE)
        ma = {}
        p = ctypes.addressof(ctypes.c_char.from_buffer(r))
        got_address = p + len(allocs)*pagesize
        print(hex(got_address))
        for i, m in enumerate(allocs):
            start = i * pagesize
            for s in m:
                ma[s] = p + start
                offset, size = sections[s].sh_offset, sections[s].sh_size
                ctypes.memmove(p+start, mm[offset:], size)
                start += size
                start = (start + alignment - 1) & -alignment

        got_sym_address = {}
        # got_table =  (ctypes.c_uint64*(4096//8)).from_buffer(r[got_address:])
        got_table = ctypes.cast(got_address, ctypes.POINTER(ctypes.c_uint64*(4096//8)))
        for i, g in enumerate(got):
            info = symbolinfo[g]
            print("INFO", info.st_shndx)
            if info.st_shndx == 0:
                # lib = ctypes.addressof()
                print(g)
                lib = ctypes.cast(libs[list(symbols.keys())[g]], ctypes.c_void_p).value
                print('lib', hex(lib))
            else:
                lib = ma[info.st_shndx] + info.st_value
            got_table.contents[i] = lib
            got_sym_address[g] = i*8
        print(got_table.contents)
        print(got_sym_address)


        # print(ma)

        load_start = ma[section_names[name]]
        for rel in relocations:
            sidx = rel.r_info >> 32
            ts = rel.r_info & 0xffffffff
            symbol = symbolinfo[sidx]
            mem = ctypes.cast(load_start + rel.r_offset, ctypes.POINTER(ctypes.c_int32))
            if ts == elf.R_X86_64_PC32:
                saddress = ma[symbol.st_shndx] + symbol.st_value
                print(hex(ma[symbol.st_shndx]))
                mem.contents.value = saddress + rel.r_addend - (load_start + rel.r_offset)
                print(hex(saddress + rel.r_addend - (load_start + rel.r_offset)))
            elif ts == elf.R_X86_64_REX_GOTPCRELX:
                mem.contents.value = got_sym_address[sidx] + got_address + rel.r_addend - (load_start + rel.r_offset)
                print(hex(got_sym_address[sidx] + got_address + rel.r_addend - (load_start + rel.r_offset)))


        result = mprotect(load_start, len(allocs)*pagesize, mmap.PROT_READ | mmap.PROT_EXEC, 0)
        if result < 0:
            print("failed")

        # ptr = ctypes.create_string_buffer(1024)
        # ptr2 = ctypes.create_string_buffer(1024)
        f = np.arange(1, 11, dtype=np.float64)
        f16 = np.zeros(10, dtype=np.float16)
        ptr, readonly = f.__array_interface__['data']
        ptr2, readonly2 = f16.__array_interface__['data']
        print(readonly, readonly2)
        print(hex(ptr), hex(ptr2))
        func = symbolinfo[symbols['copy']].st_value
        print("func addr", hex(load_start + func))
        cfunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(load_start + func)
        cfunc(ptr, ptr2)
        # a = np.frombuffer(ptr2, np.float16)
        print(f)
        print(f16)

    pprint(symbols)
    load('.text')
    print()
