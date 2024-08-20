ASM_COMPILER := nasm
C_COMPILER := gcc
ASM_FLAGS := -f elf32
C_FLAGS := -no-pie -m32

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
macro_file := $(ROOT_DIR)/macro.c

compile:
	$(ASM_COMPILER) $(ASM_FLAGS) $(DIR)/$(FILE) -o $(DIR)/$(COMPILED_FILE).o
	$(C_COMPILER) $(C_FLAGS) -c $(macro_file) -o $(DIR)/macro.o
	$(C_COMPILER) $(C_FLAGS) $(DIR)/$(COMPILED_FILE).o $(DIR)/macro.o -o $(DIR)/$(COMPILED_FILE)
run:
	$(DIR)/$(COMPILED_FILE) > $(DIR)/$(OUTPUT_FILE)
clear:
	rm $(DIR)/$(COMPILED_FILE) $(DIR)/$(OUTPUT_FILE) $(DIR)/macro.o $(DIR)/$(COMPILED_FILE).o
