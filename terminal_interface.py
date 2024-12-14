from memory_manager import MemoryManager

def terminal_interface():
    print("\nBem-vindo ao Gerenciador de Memória!")
    memory_size = int(input("Digite o tamanho da memória: "))
    manager = MemoryManager(memory_size)

    while True:
        print("\nEscolha uma opção:")
        print("1. Alocar processo (First Fit)")
        print("2. Alocar processo (Next Fit)")
        print("3. Alocar processo (Best Fit)")
        print("4. Alocar processo (Quick Fit)")
        print("5. Alocar processo (Worst Fit)")
        print("6. Desalocar processo")
        print("7. Exibir mapa de memória")
        print("8. Ver fragmentação externa")
        print("9. Sair")

        choice = input("Opção: ")

        if choice in ["1", "2", "3", "4", "5"]:
            process_id = int(input("ID do processo: "))
            process_size = int(input("Tamanho do processo: "))
            if choice == "1":
                manager.allocate_process(process_id, process_size, manager.first_fit)
            elif choice == "2":
                manager.allocate_process(process_id, process_size, manager.next_fit)
            elif choice == "3":
                manager.allocate_process(process_id, process_size, manager.best_fit)
            elif choice == "4":
                manager.allocate_process(process_id, process_size, manager.quick_fit)
            elif choice == "5":
                manager.allocate_process(process_id, process_size, manager.worst_fit)
        elif choice == "6":
            process_id = int(input("ID do processo: "))
            manager.deallocate(process_id)
        elif choice == "7":
            manager.display_memory()
        elif choice == "8":
            min_size = int(input("Tamanho mínimo de processo para fragmentação externa: "))
            manager.calculate_external_fragmentation(min_size)
        elif choice == "9":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    terminal_interface()
