uwsgi-bind-vector
==============

This project demonstrates an issue with object finalization in pybind11 when the Python interpreter is reset.

Installation
------------

Install `valgrind` if not already installed.

- clone this repository
- `cd uwsgi-bind-vector`
- `python -m venv venv`
- `source venv/bin/activate`
- `env SKBUILD_CONFIGURE_OPTIONS="-DCMAKE_BUILD_TYPE=Debug" pip install .`

Execution
---------

- `cd web`
- `valgrind uwsgi --master --plugin python310 --http :8000 --virtualenv ../venv/ --module web.wsgi --max-requests 1`

Then open localhost:8000 and hit Refresh until the stacktrace appears or about 50 times, then hit Ctrl+C.

The error is easier to reproduce with valgrind.

Typical stack trace:

```
==140923== Invalid read of size 8
==140923==    at 0xBF06C96: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_find_before_node(unsigned long, std::type_index const&, unsigned long) const (hashtable.h:1833)
==140923==    by 0xBEFF15F: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_erase(std::integral_constant<bool, true>, std::type_index const&) (hashtable.h:2203)
==140923==    by 0xBEF7F82: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::erase(std::type_index const&) (hashtable.h:938)
==140923==    by 0xBEF2DC4: std::unordered_map<std::type_index, pybind11::detail::type_info*, std::hash<std::type_index>, std::equal_to<std::type_index>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> > >::erase(std::type_index const&) (unordered_map.h:763)
==140923==    by 0xBEE6DF2: pybind11_meta_dealloc (class.h:218)
==140923==    by 0x530FB37: ??? (in /usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0)
==140923==    by 0x52E6E2D: ??? (in /usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0)
==140923==    by 0x52E8E94: Py_FinalizeEx (in /usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0)
==140923==    by 0x1964E0: uwsgi_plugins_atexit (in /home/jb/src/uwsgi-bind-vector/venv/bin/uwsgi)
==140923==    by 0x5700494: __run_exit_handlers (exit.c:113)
==140923==    by 0x570060F: exit (exit.c:143)
==140923==    by 0x14A484: uwsgi_exit (in /home/jb/src/uwsgi-bind-vector/venv/bin/uwsgi)
==140923==  Address 0x9733cf8 is 88 bytes inside a block of size 104 free'd
==140923==    at 0x484BB6F: operator delete(void*, unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==140923==    by 0xBF1702E: __gnu_cxx::new_allocator<std::__detail::_Hash_node_base*>::deallocate(std::__detail::_Hash_node_base**, unsigned long) (new_allocator.h:145)
==140923==    by 0xBF0D15F: std::allocator_traits<std::allocator<std::__detail::_Hash_node_base*> >::deallocate(std::allocator<std::__detail::_Hash_node_base*>&, std::__detail::_Hash_node_base**, unsigned long) (alloc_traits.h:496)
==140923==    by 0xBF050E4: std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<std::type_index const, pybind11::detail::type_info*>, false> > >::_M_deallocate_buckets(std::__detail::_Hash_node_base**, unsigned long) (hashtable_policy.h:1942)
==140923==    by 0xBEFD177: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_deallocate_buckets(std::__detail::_Hash_node_base**, unsigned long) (hashtable.h:449)
==140923==    by 0xBEF59BB: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_deallocate_buckets() (hashtable.h:454)
==140923==    by 0xBEF00E3: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable() (hashtable.h:1533)
==140923==    by 0xBEE0EB1: std::unordered_map<std::type_index, pybind11::detail::type_info*, std::hash<std::type_index>, std::equal_to<std::type_index>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> > >::~unordered_map() (unordered_map.h:102)
==140923==    by 0xBEE2575: pybind11::detail::local_internals::~local_internals() (internals.h:485)
==140923==    by 0x5700494: __run_exit_handlers (exit.c:113)
==140923==    by 0x570060F: exit (exit.c:143)
==140923==    by 0x14A484: uwsgi_exit (in /home/jb/src/uwsgi-bind-vector/venv/bin/uwsgi)
==140923==  Block was alloc'd at
==140923==    at 0x4849013: operator new(unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==140923==    by 0xBF246F5: __gnu_cxx::new_allocator<std::__detail::_Hash_node_base*>::allocate(unsigned long, void const*) (new_allocator.h:127)
==140923==    by 0xBF22234: std::allocator_traits<std::allocator<std::__detail::_Hash_node_base*> >::allocate(std::allocator<std::__detail::_Hash_node_base*>&, unsigned long) (alloc_traits.h:464)
==140923==    by 0xBF1E7AE: std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<std::type_index const, pybind11::detail::type_info*>, false> > >::_M_allocate_buckets(unsigned long) (hashtable_policy.h:1927)
==140923==    by 0xBF1943E: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_allocate_buckets(unsigned long) (hashtable.h:440)
==140923==    by 0xBF10E58: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_rehash_aux(unsigned long, std::integral_constant<bool, true>) (hashtable.h:2382)
==140923==    by 0xBF09935: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_rehash(unsigned long, unsigned long const&) (hashtable.h:2361)
==140923==    by 0xBF01793: std::_Hashtable<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::_M_insert_unique_node(unsigned long, unsigned long, std::__detail::_Hash_node<std::pair<std::type_index const, pybind11::detail::type_info*>, false>*, unsigned long) (hashtable.h:2021)
==140923==    by 0xBEFA426: std::__detail::_Map_base<std::type_index, std::pair<std::type_index const, pybind11::detail::type_info*>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> >, std::__detail::_Select1st, std::equal_to<std::type_index>, std::hash<std::type_index>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](std::type_index const&) (hashtable_policy.h:714)
==140923==    by 0xBEF4B64: std::unordered_map<std::type_index, pybind11::detail::type_info*, std::hash<std::type_index>, std::equal_to<std::type_index>, std::allocator<std::pair<std::type_index const, pybind11::detail::type_info*> > >::operator[](std::type_index const&) (unordered_map.h:980)
==140923==    by 0xBEEE7DD: pybind11::detail::generic_type::initialize(pybind11::detail::type_record const&) (pybind11.h:1342)
==140923==    by 0xBEFB8AE: pybind11::class_<std::vector<pod, std::allocator<pod> >, std::unique_ptr<std::vector<pod, std::allocator<pod> >, std::default_delete<std::vector<pod, std::allocator<pod> > > > >::class_<pybind11::module_local>(pybind11::handle, char const*, pybind11::module_local const&) (pybind11.h:1556)
==140923==
```