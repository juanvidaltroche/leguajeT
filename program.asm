section .data
section .bss
section .text
global _start
_start:
mov rax, 10
mov qword [rbp-8], rax
mov rax, 20
mov qword [rbp-16], rax
mov rax, qword [rbp-8]
push rax
mov rax, qword [rbp-16]
push rax
mov rax, 2
pop rbx
imul rax, rbx
pop rbx
add rax, rbx
mov qword [rbp-24], rax
mov rax, 60
xor rdi, rdi
syscall

print_number:
    ; código para imprimir un número
    ret
        