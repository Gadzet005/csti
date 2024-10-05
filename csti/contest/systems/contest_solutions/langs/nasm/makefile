ASM_COMPILER := nasm
C_COMPILER := gcc
ASM_FLAGS := -f elf32
C_FLAGS := -no-pie -m32

makeDir := $(dir $(firstword $(MAKEFILE_LIST)))
macroFile := $(makeDir)macro.c

dir := $(dir $(filePath))
fileName := $(basename $(notdir $(filePath)))

compiledPath := $(dir)$(fileName)-cmp
outputPath := $(dir)$(outputFile)

macroObjFile := $(dir)macro.o
inputObjFile := $(dir)$(fileName).o

compile:
	$(ASM_COMPILER) $(ASM_FLAGS) $(filePath) -o $(inputObjFile)
	$(C_COMPILER) $(C_FLAGS) -c $(macroFile) -o $(macroObjFile)
	$(C_COMPILER) $(C_FLAGS) $(inputObjFile) $(macroObjFile) -o $(compiledPath)
run:
	$(compiledPath) > $(outputPath)
clear:
	rm -f $(compiledPath) $(outputPath) $(macroObjFile) $(inputObjFile)
