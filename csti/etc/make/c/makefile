COMPILER := gcc
FLAGS := 	-O2 -Wall -Werror -Wformat-security -Wignored-qualifiers -Winit-self -Wswitch-default \
			-Wfloat-equal -Wpointer-arith -Wtype-limits -Wempty-body -Wno-logical-op \
			-Wstrict-prototypes -Wold-style-declaration -Wold-style-definition \
			-Wmissing-parameter-type -Wmissing-field-initializers -Wnested-externs \
			-Wno-pointer-sign -Wno-unused-result -std=gnu99 -lm

makeDir := $(dir $(firstword $(MAKEFILE_LIST)))
dir := $(dir $(filePath))
fileName := $(basename $(notdir $(filePath)))

compiledPath := $(dir)$(fileName)-cmp
outputPath := $(dir)$(outputFile)
formattedPath := $(dir)$(formattedFile)

ifeq ($(formatStyle), msu-style)
formatCommand := clang-format --style=file:$(makeDir)msu_style_config.yaml $(filePath) > $(formattedPath)
else
formatCommand := cat $(filePath) > $(dir)/$(formattedFile)
endif

compile:
	$(COMPILER) $(FLAGS) $(filePath) -o $(compiledPath)
run:
	$(compiledPath) > $(outputPath)
format:
	$(formatCommand)
clear:
	rm -f $(compiledPath) $(outputPath)
