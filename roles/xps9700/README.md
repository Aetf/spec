# Quirks in XPS 17 (9700)

## S3 Sleep
S3 sleep can be enabled by `mem_sleep_default=deep` kernel parameter.

But at least `pre-boot -> early sign of life` in BIOS config has to be disabled. Otherwise, the system
only wakes up with a corrupted logo image and the screen does not work (if there's an external screen,
you can see that the OS is actually working, just the builtin screen not working).
