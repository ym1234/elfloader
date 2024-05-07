# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-std=c99']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                if not hasattr(type_, "as_dict"):
                    value = [v for v in value]
                else:
                    type_ = type_._type_
                    value = [type_.as_dict(v) for v in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass





Elf32_Half = ctypes.c_uint16
Elf64_Half = ctypes.c_uint16
Elf32_Word = ctypes.c_uint32
Elf32_Sword = ctypes.c_int32
Elf64_Word = ctypes.c_uint32
Elf64_Sword = ctypes.c_int32
Elf32_Xword = ctypes.c_uint64
Elf32_Sxword = ctypes.c_int64
Elf64_Xword = ctypes.c_uint64
Elf64_Sxword = ctypes.c_int64
Elf32_Addr = ctypes.c_uint32
Elf64_Addr = ctypes.c_uint64
Elf32_Off = ctypes.c_uint32
Elf64_Off = ctypes.c_uint64
Elf32_Section = ctypes.c_uint16
Elf64_Section = ctypes.c_uint16
Elf32_Versym = ctypes.c_uint16
Elf64_Versym = ctypes.c_uint16
class struct_Elf32_Ehdr(Structure):
    pass

struct_Elf32_Ehdr._pack_ = 1 # source:False
struct_Elf32_Ehdr._fields_ = [
    ('e_ident', ctypes.c_ubyte * 16),
    ('e_type', ctypes.c_uint16),
    ('e_machine', ctypes.c_uint16),
    ('e_version', ctypes.c_uint32),
    ('e_entry', ctypes.c_uint32),
    ('e_phoff', ctypes.c_uint32),
    ('e_shoff', ctypes.c_uint32),
    ('e_flags', ctypes.c_uint32),
    ('e_ehsize', ctypes.c_uint16),
    ('e_phentsize', ctypes.c_uint16),
    ('e_phnum', ctypes.c_uint16),
    ('e_shentsize', ctypes.c_uint16),
    ('e_shnum', ctypes.c_uint16),
    ('e_shstrndx', ctypes.c_uint16),
]

Elf32_Ehdr = struct_Elf32_Ehdr
class struct_Elf64_Ehdr(Structure):
    pass

struct_Elf64_Ehdr._pack_ = 1 # source:False
struct_Elf64_Ehdr._fields_ = [
    ('e_ident', ctypes.c_ubyte * 16),
    ('e_type', ctypes.c_uint16),
    ('e_machine', ctypes.c_uint16),
    ('e_version', ctypes.c_uint32),
    ('e_entry', ctypes.c_uint64),
    ('e_phoff', ctypes.c_uint64),
    ('e_shoff', ctypes.c_uint64),
    ('e_flags', ctypes.c_uint32),
    ('e_ehsize', ctypes.c_uint16),
    ('e_phentsize', ctypes.c_uint16),
    ('e_phnum', ctypes.c_uint16),
    ('e_shentsize', ctypes.c_uint16),
    ('e_shnum', ctypes.c_uint16),
    ('e_shstrndx', ctypes.c_uint16),
]

Elf64_Ehdr = struct_Elf64_Ehdr
class struct_Elf32_Shdr(Structure):
    pass

struct_Elf32_Shdr._pack_ = 1 # source:False
struct_Elf32_Shdr._fields_ = [
    ('sh_name', ctypes.c_uint32),
    ('sh_type', ctypes.c_uint32),
    ('sh_flags', ctypes.c_uint32),
    ('sh_addr', ctypes.c_uint32),
    ('sh_offset', ctypes.c_uint32),
    ('sh_size', ctypes.c_uint32),
    ('sh_link', ctypes.c_uint32),
    ('sh_info', ctypes.c_uint32),
    ('sh_addralign', ctypes.c_uint32),
    ('sh_entsize', ctypes.c_uint32),
]

Elf32_Shdr = struct_Elf32_Shdr
class struct_Elf64_Shdr(Structure):
    pass

struct_Elf64_Shdr._pack_ = 1 # source:False
struct_Elf64_Shdr._fields_ = [
    ('sh_name', ctypes.c_uint32),
    ('sh_type', ctypes.c_uint32),
    ('sh_flags', ctypes.c_uint64),
    ('sh_addr', ctypes.c_uint64),
    ('sh_offset', ctypes.c_uint64),
    ('sh_size', ctypes.c_uint64),
    ('sh_link', ctypes.c_uint32),
    ('sh_info', ctypes.c_uint32),
    ('sh_addralign', ctypes.c_uint64),
    ('sh_entsize', ctypes.c_uint64),
]

Elf64_Shdr = struct_Elf64_Shdr
class struct_Elf32_Chdr(Structure):
    pass

struct_Elf32_Chdr._pack_ = 1 # source:False
struct_Elf32_Chdr._fields_ = [
    ('ch_type', ctypes.c_uint32),
    ('ch_size', ctypes.c_uint32),
    ('ch_addralign', ctypes.c_uint32),
]

Elf32_Chdr = struct_Elf32_Chdr
class struct_Elf64_Chdr(Structure):
    pass

struct_Elf64_Chdr._pack_ = 1 # source:False
struct_Elf64_Chdr._fields_ = [
    ('ch_type', ctypes.c_uint32),
    ('ch_reserved', ctypes.c_uint32),
    ('ch_size', ctypes.c_uint64),
    ('ch_addralign', ctypes.c_uint64),
]

Elf64_Chdr = struct_Elf64_Chdr
class struct_Elf32_Sym(Structure):
    pass

struct_Elf32_Sym._pack_ = 1 # source:False
struct_Elf32_Sym._fields_ = [
    ('st_name', ctypes.c_uint32),
    ('st_value', ctypes.c_uint32),
    ('st_size', ctypes.c_uint32),
    ('st_info', ctypes.c_ubyte),
    ('st_other', ctypes.c_ubyte),
    ('st_shndx', ctypes.c_uint16),
]

Elf32_Sym = struct_Elf32_Sym
class struct_Elf64_Sym(Structure):
    pass

struct_Elf64_Sym._pack_ = 1 # source:False
struct_Elf64_Sym._fields_ = [
    ('st_name', ctypes.c_uint32),
    ('st_info', ctypes.c_ubyte),
    ('st_other', ctypes.c_ubyte),
    ('st_shndx', ctypes.c_uint16),
    ('st_value', ctypes.c_uint64),
    ('st_size', ctypes.c_uint64),
]

Elf64_Sym = struct_Elf64_Sym
class struct_Elf32_Syminfo(Structure):
    pass

struct_Elf32_Syminfo._pack_ = 1 # source:False
struct_Elf32_Syminfo._fields_ = [
    ('si_boundto', ctypes.c_uint16),
    ('si_flags', ctypes.c_uint16),
]

Elf32_Syminfo = struct_Elf32_Syminfo
class struct_Elf64_Syminfo(Structure):
    pass

struct_Elf64_Syminfo._pack_ = 1 # source:False
struct_Elf64_Syminfo._fields_ = [
    ('si_boundto', ctypes.c_uint16),
    ('si_flags', ctypes.c_uint16),
]

Elf64_Syminfo = struct_Elf64_Syminfo
class struct_Elf32_Rel(Structure):
    pass

struct_Elf32_Rel._pack_ = 1 # source:False
struct_Elf32_Rel._fields_ = [
    ('r_offset', ctypes.c_uint32),
    ('r_info', ctypes.c_uint32),
]

Elf32_Rel = struct_Elf32_Rel
class struct_Elf64_Rel(Structure):
    pass

struct_Elf64_Rel._pack_ = 1 # source:False
struct_Elf64_Rel._fields_ = [
    ('r_offset', ctypes.c_uint64),
    ('r_info', ctypes.c_uint64),
]

Elf64_Rel = struct_Elf64_Rel
class struct_Elf32_Rela(Structure):
    pass

struct_Elf32_Rela._pack_ = 1 # source:False
struct_Elf32_Rela._fields_ = [
    ('r_offset', ctypes.c_uint32),
    ('r_info', ctypes.c_uint32),
    ('r_addend', ctypes.c_int32),
]

Elf32_Rela = struct_Elf32_Rela
class struct_Elf64_Rela(Structure):
    pass

struct_Elf64_Rela._pack_ = 1 # source:False
struct_Elf64_Rela._fields_ = [
    ('r_offset', ctypes.c_uint64),
    ('r_info', ctypes.c_uint64),
    ('r_addend', ctypes.c_int64),
]

Elf64_Rela = struct_Elf64_Rela
Elf32_Relr = ctypes.c_uint32
Elf64_Relr = ctypes.c_uint64
class struct_Elf32_Phdr(Structure):
    pass

struct_Elf32_Phdr._pack_ = 1 # source:False
struct_Elf32_Phdr._fields_ = [
    ('p_type', ctypes.c_uint32),
    ('p_offset', ctypes.c_uint32),
    ('p_vaddr', ctypes.c_uint32),
    ('p_paddr', ctypes.c_uint32),
    ('p_filesz', ctypes.c_uint32),
    ('p_memsz', ctypes.c_uint32),
    ('p_flags', ctypes.c_uint32),
    ('p_align', ctypes.c_uint32),
]

Elf32_Phdr = struct_Elf32_Phdr
class struct_Elf64_Phdr(Structure):
    pass

struct_Elf64_Phdr._pack_ = 1 # source:False
struct_Elf64_Phdr._fields_ = [
    ('p_type', ctypes.c_uint32),
    ('p_flags', ctypes.c_uint32),
    ('p_offset', ctypes.c_uint64),
    ('p_vaddr', ctypes.c_uint64),
    ('p_paddr', ctypes.c_uint64),
    ('p_filesz', ctypes.c_uint64),
    ('p_memsz', ctypes.c_uint64),
    ('p_align', ctypes.c_uint64),
]

Elf64_Phdr = struct_Elf64_Phdr
class struct_Elf32_Verdef(Structure):
    pass

struct_Elf32_Verdef._pack_ = 1 # source:False
struct_Elf32_Verdef._fields_ = [
    ('vd_version', ctypes.c_uint16),
    ('vd_flags', ctypes.c_uint16),
    ('vd_ndx', ctypes.c_uint16),
    ('vd_cnt', ctypes.c_uint16),
    ('vd_hash', ctypes.c_uint32),
    ('vd_aux', ctypes.c_uint32),
    ('vd_next', ctypes.c_uint32),
]

Elf32_Verdef = struct_Elf32_Verdef
class struct_Elf64_Verdef(Structure):
    pass

struct_Elf64_Verdef._pack_ = 1 # source:False
struct_Elf64_Verdef._fields_ = [
    ('vd_version', ctypes.c_uint16),
    ('vd_flags', ctypes.c_uint16),
    ('vd_ndx', ctypes.c_uint16),
    ('vd_cnt', ctypes.c_uint16),
    ('vd_hash', ctypes.c_uint32),
    ('vd_aux', ctypes.c_uint32),
    ('vd_next', ctypes.c_uint32),
]

Elf64_Verdef = struct_Elf64_Verdef
class struct_Elf32_Verdaux(Structure):
    pass

struct_Elf32_Verdaux._pack_ = 1 # source:False
struct_Elf32_Verdaux._fields_ = [
    ('vda_name', ctypes.c_uint32),
    ('vda_next', ctypes.c_uint32),
]

Elf32_Verdaux = struct_Elf32_Verdaux
class struct_Elf64_Verdaux(Structure):
    pass

struct_Elf64_Verdaux._pack_ = 1 # source:False
struct_Elf64_Verdaux._fields_ = [
    ('vda_name', ctypes.c_uint32),
    ('vda_next', ctypes.c_uint32),
]

Elf64_Verdaux = struct_Elf64_Verdaux
class struct_Elf32_Verneed(Structure):
    pass

struct_Elf32_Verneed._pack_ = 1 # source:False
struct_Elf32_Verneed._fields_ = [
    ('vn_version', ctypes.c_uint16),
    ('vn_cnt', ctypes.c_uint16),
    ('vn_file', ctypes.c_uint32),
    ('vn_aux', ctypes.c_uint32),
    ('vn_next', ctypes.c_uint32),
]

Elf32_Verneed = struct_Elf32_Verneed
class struct_Elf64_Verneed(Structure):
    pass

struct_Elf64_Verneed._pack_ = 1 # source:False
struct_Elf64_Verneed._fields_ = [
    ('vn_version', ctypes.c_uint16),
    ('vn_cnt', ctypes.c_uint16),
    ('vn_file', ctypes.c_uint32),
    ('vn_aux', ctypes.c_uint32),
    ('vn_next', ctypes.c_uint32),
]

Elf64_Verneed = struct_Elf64_Verneed
class struct_Elf32_Vernaux(Structure):
    pass

struct_Elf32_Vernaux._pack_ = 1 # source:False
struct_Elf32_Vernaux._fields_ = [
    ('vna_hash', ctypes.c_uint32),
    ('vna_flags', ctypes.c_uint16),
    ('vna_other', ctypes.c_uint16),
    ('vna_name', ctypes.c_uint32),
    ('vna_next', ctypes.c_uint32),
]

Elf32_Vernaux = struct_Elf32_Vernaux
class struct_Elf64_Vernaux(Structure):
    pass

struct_Elf64_Vernaux._pack_ = 1 # source:False
struct_Elf64_Vernaux._fields_ = [
    ('vna_hash', ctypes.c_uint32),
    ('vna_flags', ctypes.c_uint16),
    ('vna_other', ctypes.c_uint16),
    ('vna_name', ctypes.c_uint32),
    ('vna_next', ctypes.c_uint32),
]

Elf64_Vernaux = struct_Elf64_Vernaux
class struct_Elf32_Nhdr(Structure):
    pass

struct_Elf32_Nhdr._pack_ = 1 # source:False
struct_Elf32_Nhdr._fields_ = [
    ('n_namesz', ctypes.c_uint32),
    ('n_descsz', ctypes.c_uint32),
    ('n_type', ctypes.c_uint32),
]

Elf32_Nhdr = struct_Elf32_Nhdr
class struct_Elf64_Nhdr(Structure):
    pass

struct_Elf64_Nhdr._pack_ = 1 # source:False
struct_Elf64_Nhdr._fields_ = [
    ('n_namesz', ctypes.c_uint32),
    ('n_descsz', ctypes.c_uint32),
    ('n_type', ctypes.c_uint32),
]

Elf64_Nhdr = struct_Elf64_Nhdr
class struct_Elf32_Move(Structure):
    pass

struct_Elf32_Move._pack_ = 1 # source:False
struct_Elf32_Move._fields_ = [
    ('m_value', ctypes.c_uint64),
    ('m_info', ctypes.c_uint32),
    ('m_poffset', ctypes.c_uint32),
    ('m_repeat', ctypes.c_uint16),
    ('m_stride', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

Elf32_Move = struct_Elf32_Move
class struct_Elf64_Move(Structure):
    pass

struct_Elf64_Move._pack_ = 1 # source:False
struct_Elf64_Move._fields_ = [
    ('m_value', ctypes.c_uint64),
    ('m_info', ctypes.c_uint64),
    ('m_poffset', ctypes.c_uint64),
    ('m_repeat', ctypes.c_uint16),
    ('m_stride', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

Elf64_Move = struct_Elf64_Move
class struct_Elf32_RegInfo(Structure):
    pass

struct_Elf32_RegInfo._pack_ = 1 # source:False
struct_Elf32_RegInfo._fields_ = [
    ('ri_gprmask', ctypes.c_uint32),
    ('ri_cprmask', ctypes.c_uint32 * 4),
    ('ri_gp_value', ctypes.c_int32),
]

Elf32_RegInfo = struct_Elf32_RegInfo
class struct_Elf_Options(Structure):
    pass

struct_Elf_Options._pack_ = 1 # source:False
struct_Elf_Options._fields_ = [
    ('kind', ctypes.c_ubyte),
    ('size', ctypes.c_ubyte),
    ('section', ctypes.c_uint16),
    ('info', ctypes.c_uint32),
]

Elf_Options = struct_Elf_Options
class struct_Elf_Options_Hw(Structure):
    pass

struct_Elf_Options_Hw._pack_ = 1 # source:False
struct_Elf_Options_Hw._fields_ = [
    ('hwp_flags1', ctypes.c_uint32),
    ('hwp_flags2', ctypes.c_uint32),
]

Elf_Options_Hw = struct_Elf_Options_Hw
class struct_Elf32_Lib(Structure):
    pass

struct_Elf32_Lib._pack_ = 1 # source:False
struct_Elf32_Lib._fields_ = [
    ('l_name', ctypes.c_uint32),
    ('l_time_stamp', ctypes.c_uint32),
    ('l_checksum', ctypes.c_uint32),
    ('l_version', ctypes.c_uint32),
    ('l_flags', ctypes.c_uint32),
]

Elf32_Lib = struct_Elf32_Lib
class struct_Elf64_Lib(Structure):
    pass

struct_Elf64_Lib._pack_ = 1 # source:False
struct_Elf64_Lib._fields_ = [
    ('l_name', ctypes.c_uint32),
    ('l_time_stamp', ctypes.c_uint32),
    ('l_checksum', ctypes.c_uint32),
    ('l_version', ctypes.c_uint32),
    ('l_flags', ctypes.c_uint32),
]

Elf64_Lib = struct_Elf64_Lib
Elf32_Conflict = ctypes.c_uint32
class struct_Elf_MIPS_ABIFlags_v0(Structure):
    pass

struct_Elf_MIPS_ABIFlags_v0._pack_ = 1 # source:False
struct_Elf_MIPS_ABIFlags_v0._fields_ = [
    ('version', ctypes.c_uint16),
    ('isa_level', ctypes.c_ubyte),
    ('isa_rev', ctypes.c_ubyte),
    ('gpr_size', ctypes.c_ubyte),
    ('cpr1_size', ctypes.c_ubyte),
    ('cpr2_size', ctypes.c_ubyte),
    ('fp_abi', ctypes.c_ubyte),
    ('isa_ext', ctypes.c_uint32),
    ('ases', ctypes.c_uint32),
    ('flags1', ctypes.c_uint32),
    ('flags2', ctypes.c_uint32),
]

Elf_MIPS_ABIFlags_v0 = struct_Elf_MIPS_ABIFlags_v0

# # values for enumeration 'enum (unnamed at /usr/include/elf.h:2258:1)'
# enum (unnamed at /usr/include/elf.h:2258:1)__enumvalues = {
#     0: 'Val_GNU_MIPS_ABI_FP_ANY',
#     1: 'Val_GNU_MIPS_ABI_FP_DOUBLE',
#     2: 'Val_GNU_MIPS_ABI_FP_SINGLE',
#     3: 'Val_GNU_MIPS_ABI_FP_SOFT',
#     4: 'Val_GNU_MIPS_ABI_FP_OLD_64',
#     5: 'Val_GNU_MIPS_ABI_FP_XX',
#     6: 'Val_GNU_MIPS_ABI_FP_64',
#     7: 'Val_GNU_MIPS_ABI_FP_64A',
#     7: 'Val_GNU_MIPS_ABI_FP_MAX',
# }
# Val_GNU_MIPS_ABI_FP_ANY = 0
# Val_GNU_MIPS_ABI_FP_DOUBLE = 1
# Val_GNU_MIPS_ABI_FP_SINGLE = 2
# Val_GNU_MIPS_ABI_FP_SOFT = 3
# Val_GNU_MIPS_ABI_FP_OLD_64 = 4
# Val_GNU_MIPS_ABI_FP_XX = 5
# Val_GNU_MIPS_ABI_FP_64 = 6
# Val_GNU_MIPS_ABI_FP_64A = 7
# Val_GNU_MIPS_ABI_FP_MAX = 7
# enum (unnamed at /usr/include/elf.h:2258:1) = ctypes.c_uint32 # enum
__all__ = \
    ['Elf32_Addr', 'Elf32_Chdr', 'Elf32_Conflict', 'Elf32_Dyn',
    'Elf32_Ehdr', 'Elf32_Half', 'Elf32_Lib', 'Elf32_Move',
    'Elf32_Nhdr', 'Elf32_Off', 'Elf32_Phdr', 'Elf32_RegInfo',
    'Elf32_Rel', 'Elf32_Rela', 'Elf32_Relr', 'Elf32_Section',
    'Elf32_Shdr', 'Elf32_Sword', 'Elf32_Sxword', 'Elf32_Sym',
    'Elf32_Syminfo', 'Elf32_Verdaux', 'Elf32_Verdef', 'Elf32_Vernaux',
    'Elf32_Verneed', 'Elf32_Versym', 'Elf32_Word', 'Elf32_Xword',
    'Elf32_auxv_t', 'Elf32_gptab', 'Elf64_Addr', 'Elf64_Chdr',
    'Elf64_Dyn', 'Elf64_Ehdr', 'Elf64_Half', 'Elf64_Lib',
    'Elf64_Move', 'Elf64_Nhdr', 'Elf64_Off', 'Elf64_Phdr',
    'Elf64_Rel', 'Elf64_Rela', 'Elf64_Relr', 'Elf64_Section',
    'Elf64_Shdr', 'Elf64_Sword', 'Elf64_Sxword', 'Elf64_Sym',
    'Elf64_Syminfo', 'Elf64_Verdaux', 'Elf64_Verdef', 'Elf64_Vernaux',
    'Elf64_Verneed', 'Elf64_Versym', 'Elf64_Word', 'Elf64_Xword',
    'Elf64_auxv_t', 'Elf_MIPS_ABIFlags_v0', 'Elf_Options',
    'Elf_Options_Hw', 'Val_GNU_MIPS_ABI_FP_64',
    'Val_GNU_MIPS_ABI_FP_64A', 'Val_GNU_MIPS_ABI_FP_ANY',
    'Val_GNU_MIPS_ABI_FP_DOUBLE', 'Val_GNU_MIPS_ABI_FP_MAX',
    'Val_GNU_MIPS_ABI_FP_OLD_64', 'Val_GNU_MIPS_ABI_FP_SINGLE',
    'Val_GNU_MIPS_ABI_FP_SOFT', 'Val_GNU_MIPS_ABI_FP_XX', 'struct_Elf32_Chdr',
    'struct_Elf32_Dyn', 'struct_Elf32_Ehdr', 'struct_Elf32_Lib',
    'struct_Elf32_Move', 'struct_Elf32_Nhdr', 'struct_Elf32_Phdr',
    'struct_Elf32_RegInfo', 'struct_Elf32_Rel', 'struct_Elf32_Rela',
    'struct_Elf32_Shdr', 'struct_Elf32_Sym', 'struct_Elf32_Syminfo',
    'struct_Elf32_Verdaux', 'struct_Elf32_Verdef',
    'struct_Elf32_Vernaux', 'struct_Elf32_Verneed',
    'struct_Elf32_auxv_t', 'struct_Elf64_Chdr', 'struct_Elf64_Dyn',
    'struct_Elf64_Ehdr', 'struct_Elf64_Lib', 'struct_Elf64_Move',
    'struct_Elf64_Nhdr', 'struct_Elf64_Phdr', 'struct_Elf64_Rel',
    'struct_Elf64_Rela', 'struct_Elf64_Shdr', 'struct_Elf64_Sym',
    'struct_Elf64_Syminfo', 'struct_Elf64_Verdaux',
    'struct_Elf64_Verdef', 'struct_Elf64_Vernaux',
    'struct_Elf64_Verneed', 'struct_Elf64_auxv_t',
    'struct_Elf_MIPS_ABIFlags_v0', 'struct_Elf_Options',
    'struct_Elf_Options_Hw', 'union_Elf32_gptab']
