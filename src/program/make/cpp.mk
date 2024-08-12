COMPILER := g++
FLAGS := -O2 -Wall -Werror

compile:
	$(COMPILER) $(FLAGS) $(DIR)/$(FILE) -o $(DIR)/$(COMPILED_FILE)
run:
	$(DIR)/$(COMPILED_FILE) > $(DIR)/$(OUTPUT_FILE)
format:
	clang-format --style=file:$(FORMAT_CONFIG) $(DIR)/$(FILE) > $(DIR)/$(FORMATTED_FILE)
clear:
	rm $(DIR)/$(COMPILED_FILE) $(DIR)/$(OUTPUT_FILE)
