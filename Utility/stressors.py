cpu_stressors="af-alg atomic bitonicsort branch bsearch context cpu cpu-online crypt eigen factor fma fp fp-error funccall funcret getrandom goto hash heapsort hsearch ioport ipsec-mb jpeg judy list longjmp lsearch matrix matrix-3d mergesort monte-carlo mpfr nop numa opcode plugin prefetch priv-instr qsort radixsort rdrand regs rotate rseq secretmem shellsort skiplist smi sparsematrix str stream syncload tree trig tsc tsearch uprobe vecfp vecmath vecshuf vecwide vnni waitcpu wcs x86cpuid zlib"
io_stressors="aio aiol hdd io-uring rawdev readahead revio seek sync-file"
filesystem_stressors="access acl bind-mount binderfs chattr chdir chmod chown copy-file dentry dir dirdeep dirmany dnotify dup eventfd fallocate fanotify fcntl fd-fork fiemap file-ioctl filename flock fpunch fsize fstat getdent handle hdd inode-flags inotify io iomix ioprio lease link locka lockf lockofd metamix mknod open procfs rename symlink sync-file touch utime verity xattr"
memory_stressors="atomic bad-altstack bitonicsort bsearch context full heapsort hsearch judy list lockbus lsearch malloc matrix matrix-3d mcontend membarrier memcpy memfd memrate memthrash mergesort mincore misaligned null numa oom-pipe pipe pipeherd prefetch qsort radixsort randlist remap resources rmap shellsort skiplist sparsematrix stack stackmmap str stream tlb-shootdown tmpfs tree tsearch vm vm-addr vm-rw vm-segv wcs zero zlib"
scheduler_stressors="affinity clone cyclic daemon dnotify eventfd exec exit-group fanotify fault fifo fork forkheavy futex hrtimers inotify kill loadavg mmapfork mq msg mutex nanosleep netlink-proc netlink-task nice poll prio-inv pthread race-sched resched schedmix schedpolicy sem sem-sysv session sleep softlockup spawn switch tee vfork vforkmany wait workload yield zombie"
stressors = []
stressors.append(cpu_stressors)
stressors.append(io_stressors)
stressors.append(filesystem_stressors)
stressors.append(memory_stressors)
stressors.append(scheduler_stressors)

for string in stressors :
    string = string.replace(" ", "\" \"")
    string = "\"" + string + "\""
    print(string+"\n")