import mmap
import elf
import ctypes
from pprint import pprint
from contextlib import closing

pagesize = mmap.PAGESIZE

libc = ctypes.cdll.LoadLibrary(None)
lmmap = libc.mmap
lmmap.restype = ctypes.c_void_p
lmmap.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_size_t)

mprotect = libc.mprotect
mprotect.restype = ctypes.c_int
mprotect.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int)


with open('mainfp16.o') as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY)
    hdr = elf.Elf64_Ehdr.from_buffer(mm)
    sections = (elf.Elf64_Shdr*hdr.e_shnum).from_buffer(mm, hdr.e_shoff)
    shstroff = sections[hdr.e_shstrndx].sh_offset
    section_names = {ctypes.string_at(mm[shstroff + s.sh_name:]).decode('ascii'): i for i, s in enumerate(sections)}
    pprint(section_names)
    symtabhdr = sections[section_names['.symtab']]
    strtabhdr = sections[section_names['.strtab']]

    nsymbols = symtabhdr.sh_size // symtabhdr.sh_entsize
    symbolinfo = (elf.Elf64_Sym*nsymbols).from_buffer(mm, symtabhdr.sh_offset);

    symbols = {ctypes.string_at(mm[strtabhdr.sh_offset + s.st_name:]).decode('ascii'): i for i, s in enumerate(symbolinfo)}
    def load(name):
        section = sections[section_names[name]]
        if '.rela'+name not in section_names:
            return section
        relhdr = sections[section_names['.rela'+name]]
        nrel = relhdr.sh_size // relhdr.sh_entsize
        relocations = (elf.Elf64_Rela*nrel).from_buffer(mm, relhdr.sh_offset)
        relsections = []
        for rel in relocations:
            sidx = rel.r_info >> 32
            ts = rel.r_info & 0xffffffff
            relsections.append(symbolinfo[sidx].st_shndx)
            # print(ctypes.string_at(mm[strtabhdr.sh_offset + symbolinfo[sidx].st_name:]).decode('ascii'), ts)
            # print(sidx, ts)
            # pass
        allocs = [[section_names[name]]]
        sum = section.sh_size
        for s in relsections:
            print(sum)
            if sum + sections[s].sh_size < pagesize:
                allocs[-1].append(s)
                sum += sections[s].sh_size
                sum = (sum + 7) & -8
            else:
                allocs.append([])
                sum = (sections[s].sh_size + 7) & -8

        print(sum)
        print(allocs)
        print(relsections)
        r = mmap.mmap(-1, len(allocs)*pagesize, mmap.MAP_PRIVATE, mmap.PROT_READ | mmap.PROT_WRITE)

        ma = {}
        for i, m in enumerate(allocs):
            start = i * pagesize
            for s in m:
                ma[s] = start
                offset, size = sections[s].sh_offset, sections[s].sh_size
                ctypes.memmove(r[start:], mm[offset:], size)
                start += size
                start = (start + 7) & -8
            print(start)

        print(ctypes.c_void_p.from_buffer(r), m)
        load_start = m[section_names[name]]
        for rel in relocations:
            rel.r_offset
            sidx = rel.r_info >> 32
            ts = rel.r_info & 0xffffffff
            symbol = symbolinfo[sidx]
            ss = m[symbol.st_shndx] + symbol.st_value
    pprint(symbols)
    load('.text')
    print()
