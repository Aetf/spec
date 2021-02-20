## Aetf-Arch-XPS

### Partition layout

* The bottom layer is a 512GB partition
* Which then forms a LVM PV
* The PV is allocated to LVM VG `ArchGroup`
* Two LVs are created in the VG
    + `crypthome` remaining
    + `cryptroot` 64GB
* `crypthome`
    + Size: <448.00 GiB
    + Hosts Luks encrypted xfs partition
    + The luks key is in the root partition `/etc/luks-keys/home` and managed by `/etc/crypttab`
* `cryptroot`
    + Size: 64GB
    + Hosts Luks encrypted btrfs partition
    + Protected by password
    + btrfs subvolumes
        - `@` -> `/`
        - `@var` -> `/var`
        - `@root` -> `/root`
        - `@swapfiles` -> `/.swapfiles`
        - `@snapshots` -> `/.snapshots`
* The swap file is located at `/.swapfiles/hibernate`


#### Reasoning

The LVM is used so that we can extend and move partitions around even though Luks header can not be moved.
As the LVM maintains the mapping from PV blocks to LV blocks, and they can be nonlinear.
