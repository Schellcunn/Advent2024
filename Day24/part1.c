#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_VARS 1000

typedef struct {
    char name[10];
    int value;
    int resolved;
} Variable;

typedef struct {
    char name[10];
    char operator[4];
    char input1[10];
    char input2[10];
    int resolved;
} Gate;

Variable variables[MAX_VARS];
int var_count = 0;

char *input(FILE* fp, size_t size);
char *read_rest_of_file(FILE* fp);
void parse_line(char *line);
void evaluate_expressions(char *rest_of_file);
int get_variable_value(const char *name);
void set_variable_value(const char *name, int value);
void save_specific_variables_to_file();
int compare_variables(const void *a, const void *b);

int main() {
    FILE *file = fopen("c:/Users/User/Projektit/Advent2024/input7.txt", "r");
    char *line;
    char *rest_of_file = NULL;

    // Check if the file was opened successfully.
    if (file != NULL) {
        // Read each line from the file using the input function.
        while ((line = input(file, 128)) != NULL) {
            // Parse each line to store variable values.
            parse_line(line);
            free(line); // Free the allocated memory for the line.
        }

        // Read the rest of the file after the empty line.
        rest_of_file = read_rest_of_file(file);

        // Evaluate the expressions in the rest of the file.
        if (rest_of_file) {
            evaluate_expressions(rest_of_file);
            free(rest_of_file);
        }

        // Save the variables starting with 'z' to a file.
        save_specific_variables_to_file();

        // Close the file stream once all lines have been read.
        fclose(file);
    } else {
        // Print an error message to the standard error stream if the file cannot be opened.
        fprintf(stderr, "Unable to open file!\n");
    }

    return 0;
}

char *input(FILE* fp, size_t size) {
    char *str;
    int ch;
    size_t len = 0;
    str = realloc(NULL, sizeof(char) * size);
    if (!str) return str;
    while (EOF != (ch = fgetc(fp)) && ch != '\n') {
        str[len++] = ch;
        if (len == size) {
            str = realloc(str, sizeof(char) * (size += 16));
            if (!str) return str;
        }
    }
    if (len == 0 && ch == '\n') {
        // Empty line
        free(str);
        return NULL;
    }
    str[len++] = '\0';

    return realloc(str, sizeof(char) * len);
}

char *read_rest_of_file(FILE* fp) {
    fseek(fp, 0, SEEK_CUR); // Ensure the file pointer is at the current position
    long start_pos = ftell(fp);
    fseek(fp, 0, SEEK_END);
    long end_pos = ftell(fp);
    fseek(fp, start_pos, SEEK_SET);

    size_t size = end_pos - start_pos;
    char *buffer = malloc(size + 1);
    if (buffer) {
        fread(buffer, 1, size, fp);
        buffer[size] = '\0';
    }
    return buffer;
}

void parse_line(char *line) {
    char name[10];
    int value;
    if (sscanf(line, "%[^:]: %d", name, &value) == 2) {
        set_variable_value(name, value);
    }
}

void evaluate_expressions(char *rest_of_file) {
    Gate gates[MAX_VARS];
    int gate_count = 0;
    
    // Parse gates first
    char *line = strtok(rest_of_file, "\n");
    while (line != NULL) {
        char input1[10], op[4], input2[10], output[10];
        
        // Parse gate definition
        if (sscanf(line, "%s %s %s -> %s", input1, op, input2, output) == 4) {
            strcpy(gates[gate_count].name, output);
            strcpy(gates[gate_count].operator, op);
            strcpy(gates[gate_count].input1, input1);
            strcpy(gates[gate_count].input2, input2);
            gates[gate_count].resolved = 0;
            gate_count++;
        }
        
        line = strtok(NULL, "\n");
    }

    // Evaluate gates until no more changes
    int changes;
    do {
        changes = 0;
        for (int i = 0; i < gate_count; i++) {
            if (gates[i].resolved) continue;
            
            int val1 = get_variable_value(gates[i].input1);
            int val2 = get_variable_value(gates[i].input2);
            
            if (val1 != -1 && val2 != -1) {
                int result = 0;
                if (strcmp(gates[i].operator, "AND") == 0) {
                    result = val1 & val2;
                } else if (strcmp(gates[i].operator, "OR") == 0) {
                    result = val1 | val2;
                } else if (strcmp(gates[i].operator, "XOR") == 0) {
                    result = val1 ^ val2;
                }
                set_variable_value(gates[i].name, result);
                gates[i].resolved = 1;
                changes = 1;
            }
        }
    } while (changes);
}

int get_variable_value(const char *name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(variables[i].name, name) == 0) {
            return variables[i].value;
        }
    }
    return -1; // Return -1 if variable not found
}

void set_variable_value(const char *name, int value) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(variables[i].name, name) == 0) {
            variables[i].value = value;
            variables[i].resolved = 1;
            return;
        }
    }
    strcpy(variables[var_count].name, name);
    variables[var_count].value = value;
    variables[var_count].resolved = 1;
    var_count++;
}

int compare_variables(const void *a, const void *b) {
    return strcmp(((Variable *)a)->name, ((Variable *)b)->name);
}

void save_specific_variables_to_file() {
    Variable z_variables[MAX_VARS];
    int z_var_count = 0;
    unsigned long long decimal_value = 0;

    // Collect variables starting with 'z'
    for (int i = 0; i < var_count; i++) {
        if (variables[i].name[0] == 'z') {
            z_variables[z_var_count++] = variables[i];
        }
    }

    // Sort variables in alphabetical order
    qsort(z_variables, z_var_count, sizeof(Variable), compare_variables);

    // Calculate decimal value and create binary string
    char binary_string[MAX_VARS + 1] = {0};
    for (int i = 0; i < z_var_count; i++) {
        int bit_position = atoi(z_variables[i].name + 1);
        if (z_variables[i].value) {
            decimal_value |= (1ULL << bit_position);
            binary_string[i] = '1';
        } else {
            binary_string[i] = '0';
        }
    }

    // Write results to file
    FILE *output_file = fopen("z_variables.txt", "w");
    if (output_file == NULL) {
        fprintf(stderr, "Unable to open output file!\n");
        return;
    }

    for (int i = 0; i < z_var_count; i++) {
        fprintf(output_file, "%s: %d\n", z_variables[i].name, z_variables[i].value);
    }
    fprintf(output_file, "Binary string: %s\n", binary_string);
    fprintf(output_file, "Decimal value: %llu\n", decimal_value);
    fclose(output_file);
}