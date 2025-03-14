#!/bin/bash
# load.sh
# This script uses stress-ng to randomly run stress tests on
# different classes for varying lengths of time.

# These are the five classes that will be stressed
classes=("cpu" "io" "filesystem" "memory" "scheduler")

# These are the possible stressors for each of the classes.
# This is to be able to pick random stressors within each class, since --class and --random can't work together.
# Now, --with can be used to select random stressors from these arrays.
cpu=("af-alg" "atomic" "bitonicsort" "branch" "bsearch" "context" "cpu" "cpu-online" "crypt" "eigen" "factor" "fma" "fp" "fp-error" "funccall" "funcret" "getrandom" "goto" "hash" "heapsort" "hsearch" "ioport" "ipsec-mb" "jpeg" "judy" "list" "longjmp" "lsearch" "matrix" "matrix-3d" "mergesort" "monte-carlo" "mpfr" "nop" "numa" "opcode" "plugin" "prefetch" "priv-instr" "qsort" "radixsort" "rdrand" "regs" "rotate" "rseq" "secretmem" "shellsort" "skiplist" "smi" "sparsematrix" "str" "stream" "syncload" "tree" "trig" "tsc" "tsearch" "uprobe" "vecfp" "vecmath" "vecshuf" "vecwide" "vnni" "waitcpu" "wcs" "x86cpuid" "zlib")

io=("aio" "aiol" "hdd" "io-uring" "rawdev" "readahead" "revio" "seek" "sync-file")

filesystem=("access" "acl" "bind-mount" "binderfs" "chattr" "chdir" "chmod" "chown" "copy-file" "dentry" "dir" "dirdeep" "dirmany" "dnotify" "dup" "eventfd" "fallocate" "fanotify" "fcntl" "fd-fork" "fiemap" "file-ioctl" "filename" "flock" "fpunch" "fsize" "fstat" "getdent" "handle" "hdd" "inode-flags" "inotify" "io" "iomix" "ioprio" "lease" "link" "locka" "lockf" "lockofd" "metamix" "mknod" "open" "procfs" "rename" "symlink" "sync-file" "touch" "utime" "verity" "xattr")

memory=("atomic" "bad-altstack" "bitonicsort" "bsearch" "context" "full" "heapsort" "hsearch" "judy" "list" "lockbus" "lsearch" "malloc" "matrix" "matrix-3d" "mcontend" "membarrier" "memcpy" "memfd" "memrate" "memthrash" "mergesort" "mincore" "misaligned" "null" "numa" "oom-pipe" "pipe" "pipeherd" "prefetch" "qsort" "radixsort" "randlist" "remap" "resources" "rmap" "shellsort" "skiplist" "sparsematrix" "stack" "stackmmap" "str" "stream" "tlb-shootdown" "tmpfs" "tree" "tsearch" "vm" "vm-addr" "vm-rw" "vm-segv" "wcs" "zero" "zlib")

scheduler=("affinity" "clone" "cyclic" "daemon" "dnotify" "eventfd" "exec" "exit-group" "fanotify" "fault" "fifo" "fork" "forkheavy" "futex" "hrtimers" "inotify" "kill" "loadavg" "mmapfork" "mq" "msg" "mutex" "nanosleep" "netlink-proc" "netlink-task" "nice" "poll" "prio-inv" "pthread" "race-sched" "resched" "schedmix" "schedpolicy" "sem" "sem-sysv" "session" "sleep" "softlockup" "spawn" "switch" "tee" "vfork" "vforkmany" "wait" "workload" "yield" "zombie")

# These are the time intervals that each stress may run for
intervals=(10 15 20 25 30)
while true; do
	name=${classes[(( $RANDOM%"${#classes[@]}" ))]}
	time=$(( $RANDOM%"${#intervals[@]}" ))
	num_stressors=$(( ${intervals[time]}/5 ))
	stressors=""
	eval "array=(\"\${$name[@]}\")"
	length=${#array[@]}
	echo "Class: ${name}"; echo "Number of Stressors: ${num_stressors}"
	for (( i=0; i<$num_stressors; i++ )) do
		index="$(( RANDOM%$length ))"
		stressors+=${array[$index]}
		if (( i+1 < $num_stressors )) ; then
			stressors+=","
		fi
	done
	echo "Stressors: ${stressors}"
	stress-ng --seq 1 --with $stressors -t 5 --progress --log-file /var/log/load.log
done


