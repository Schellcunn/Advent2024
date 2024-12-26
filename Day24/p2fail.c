#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_VARS 1000

typedef struct {
    char name[10];
    int value;
    int resolved;
} Variable;

typedef struct {
    char original[100];
    char lhs[10];
    char rhs[10];
    char op[4];
    char target[10];
} Triple;

Variable variables[MAX_VARS];
int var_count = 0;

Triple triples[MAX_VARS];
int triple_count = 0;

char* invalid_gates[MAX_VARS];
int invalid_count = 0;

int compare_variables(const void *a, const void *b) {
    return strcmp(((Variable *)a)->name, ((Variable *)b)->name);
}

int compare_strings(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

void set_variable_value(const char* name, int value) {
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

void parse_gate_line(char* line) {
    char lhs[10], op[4], rhs[10], target[10];
    if (sscanf(line, "%s %s %s -> %s", lhs, op, rhs, target) == 4) {
        strcpy(triples[triple_count].original, line);
        strcpy(triples[triple_count].op, op);
        strcpy(triples[triple_count].target, target);
        
        if (strcmp(lhs, rhs) < 0) {
            strcpy(triples[triple_count].lhs, lhs);
            strcpy(triples[triple_count].rhs, rhs);
        } else {
            strcpy(triples[triple_count].lhs, rhs);
            strcpy(triples[triple_count].rhs, lhs);
        }
        triple_count++;
    }
}

int is_gate_invalid(const char* gate) {
    for (int i = 0; i < invalid_count; i++) {
        if (strcmp(invalid_gates[i], gate) == 0) {
            return 1;  // Gate already recorded as invalid
        }
    }
    return 0;  // Gate not found
}

void add_invalid_gate(const char* gate) {
    if (!is_gate_invalid(gate)) {
        invalid_gates[invalid_count++] = strdup(gate);
    }
}

void validate_rules() {
    for (int i = 0; i < triple_count; i++) {
        Triple* t = &triples[i];
        
        // Rule 1: Only XORs can target Zs
        if (t->target[0] == 'z' && strcmp(t->op, "XOR") != 0 && strcmp(t->target, "z45") != 0) {
            add_invalid_gate(t->target);
        }
        
        // Rule 2: Stage2 XORs must target Zs
        if (t->target[0] != 'z' && strcmp(t->op, "XOR") == 0 && t->lhs[0] != 'x') {
            add_invalid_gate(t->target);
        }
        
        // Rule 3: ANDs must feed ORs
        if (strcmp(t->op, "AND") == 0 && strcmp(t->lhs, "x00") != 0) {
            int feeds_or = 0;
            for (int j = 0; j < triple_count; j++) {
                if ((strcmp(triples[j].lhs, t->target) == 0 || 
                     strcmp(triples[j].rhs, t->target) == 0) &&
                    strcmp(triples[j].op, "OR") == 0) {
                    feeds_or = 1;
                    break;
                }
            }
            if (!feeds_or) {
                add_invalid_gate(t->target);
            }
        }
        
        // Rule 4: ORs must be targeted by ANDs
        if (strcmp(t->op, "OR") == 0) {
            for (int j = 0; j < triple_count; j++) {
                if (strcmp(triples[j].target, t->lhs) == 0 && strcmp(triples[j].op, "AND") != 0) {
                    add_invalid_gate(triples[j].target);
                }
                if (strcmp(triples[j].target, t->rhs) == 0 && strcmp(triples[j].op, "AND") != 0) {
                    add_invalid_gate(triples[j].target);
                }
            }
        }
    }
}

void save_specific_variables_to_file() {
    FILE *output_file = fopen("c:/Users/User/Projektit/Advent2024/Day24/invalid_gates.txt", "w");
    if (output_file == NULL) {
        fprintf(stderr, "Unable to open output file!\n");
        return;
    }

    // Sort invalid gates
    qsort(invalid_gates, invalid_count, sizeof(char*), compare_strings);
    
    // Write invalid gates
    fprintf(output_file, "Invalid gates: ");
    for (int i = 0; i < invalid_count; i++) {
        if (i > 0) fprintf(output_file, ",");
        fprintf(output_file, "%s", invalid_gates[i]);
    }
    
    fclose(output_file);
}

int main() {
    // Change input8.txt to full path
    FILE *file = fopen("c:/Users/User/Projektit/Advent2024/input7.txt", "r");
    if (!file) {
        fprintf(stderr, "Cannot open input file!\n");
        return 1;
    }
    
    // Rest of main remains the same
    char line[256];
    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\n")] = 0;  // Remove newline
        
        if (strchr(line, ':')) {  // Variable definition
            char name[10];
            int value;
            sscanf(line, "%[^:]: %d", name, &value);
            set_variable_value(name, value);
        } else if (strlen(line) > 0) {  // Gate definition
            parse_gate_line(line);
        }
    }

    validate_rules();
    save_specific_variables_to_file();

    // Cleanup
    for (int i = 0; i < invalid_count; i++) {
        free(invalid_gates[i]);
    }

    fclose(file);
    return 0;
}