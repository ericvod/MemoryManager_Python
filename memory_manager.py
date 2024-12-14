class MemoryManager:
    def __init__(self, size):
        self.memory = [0] * size
        self.size = size
        self.last_index = 0 # Para Next Fit
        self.block_sizes = {} # Para Quick Fit
        self.process_colors = {} # Mapear processos às cores
        self.ansi_palette = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]  # Paleta ANSI para terminal

    def display_memory(self):
        print("Mapa de memoria:")
        for block in self.memory:
            if block == 0:
                print("0", end=" ")
            else:
                color = self.process_colors.get(block, "\033[97m")
                print(f"{color}1\033[0m", end=" ")
        print()

    def allocate_process(self, process_id, process_size, allocation_strategy):
        if process_id in self.process_colors:
            print(f"Erro: Processo {process_id} já existe na memória.")
            return False

        color = self.ansi_palette[len(self.process_colors) % len(self.ansi_palette)]
        self.process_colors[process_id] = color

        success = allocation_strategy(process_id, process_size)
        if not success:
            del self.process_colors[process_id]
        return success


    def first_fit(self, process_id, process_size):
        for i in range(self.size - process_size + 1):
            if all(block == 0 for block in self.memory[i:i + process_size]):
                self.memory[i:i + process_size] = [process_id] * process_size
                print(f"Processo {process_id} alocado no bloco {i}")
                self.display_memory()
                return True
        print(f"Erro: Processo {process_id} nao pode ser alocado")
        return False

    def next_fit(self, process_id, process_size):
        start = self.last_index
        for _ in range(self.size):
            i = (start + _) % self.size
            if i + process_size <= self.size and all(block == 0 for block in self.memory[i:i + process_size]):
                self.memory[i:i + process_size] = [process_id] * process_size
                self.last_index = i + process_size
                print(f"Processo {process_id} alocado no bloco {i}")
                self.display_memory()
                return True
        print(f"Erro: Processo {process_id} nao pode ser alocado")
        return False

    def best_fit(self, process_id, process_size):
        best_start = None
        best_size = float('inf')
        i = 0
        while i < self.size:
            if self.memory[i] == 0:
                start = i
                while i < self.size and self.memory[i] == 0:
                    i += 1
                hole_size = i - start
                if process_size <= hole_size < best_size:
                    best_start = start
                    best_size = hole_size
            else:
                i += 1
        if best_start is not None:
            self.memory[best_start:best_start + process_size] = [process_id] * process_size
            print(f"Processo {process_id} alocado no bloco {best_start}")
            self.display_memory()
            return True
        print(f"Erro: Processo {process_id} nao pode ser alocado")
        return False

    def quick_fit(self, process_id, process_size):
        self.update_quick_fit()

        suitable_holes = [size for size in self.block_sizes if size >= process_size]
        if not suitable_holes:
            print(f"Erro: Processo {process_id} nao pode ser alocado")
            return False

        suitable_holes.sort()
        chosen_size = suitable_holes[0]
        start = self.block_sizes[chosen_size].pop(0)
        if not self.block_sizes[chosen_size]:
            del self.block_sizes[chosen_size]

        self.memory[start:start + process_size] = [process_id] * process_size
        remaining_size = chosen_size - process_size
        if remaining_size > 0:
            new_start = start + process_size
            if remaining_size not in self.block_sizes:
                self.block_sizes[remaining_size] = []
            self.block_sizes[remaining_size].append(new_start)

        print(f"Processo {process_id} alocado no bloco {start}")
        self.display_memory()
        return True

    def update_quick_fit(self):
        self.block_sizes.clear()
        i = 0
        while i < self.size:
            if self.memory[i] == 0:
                start = i
                while i < self.size and self.memory[i] == 0:
                    i += 1
                hole_size = i - start
                if hole_size > 0:
                    if hole_size not in self.block_sizes:
                        self.block_sizes[hole_size] = []
                    self.block_sizes[hole_size].append(start)
            else:
                i += 1

    def worst_fit(self, process_id, process_size):
        worst_start = None
        worst_size = -1
        i = 0
        while i < self.size:
            if self.memory[i] == 0:
                start = i
                while i < self.size and self.memory[i] == 0:
                    i += 1
                hole_size = i - start
                if hole_size >= process_size and hole_size > worst_size:
                    worst_start = start
                    worst_size = hole_size
            else:
                i += 1
        if worst_start is not None:
            self.memory[worst_start:worst_start + process_size] = [process_id] * process_size
            print(f"Processo {process_id} alocado no bloco {worst_start}")
            self.display_memory()
            return True
        print(f"Erro: Processo {process_id} nao pode ser alocado")
        return False

    def deallocate(self, process_id):
        if process_id in self.memory:
            self.memory = [0 if block == process_id else block for block in self.memory]
            del self.process_colors[process_id]
            self.update_quick_fit()
            print(f"Processo {process_id} desalocado")
            self.display_memory()
        else:
            print(f"Erro: Processo {process_id} nao encontrado na memoria")

    def calculate_external_fragmentation(self, min_process_size):
        external_fragments = 0
        i = 0
        while i < self.size:
            if self.memory[i] == 0:
                start = i
                while i < self.size and self.memory[i] == 0:
                    i += 1
                hole_size = i - start
                if hole_size < min_process_size:
                    external_fragments += 1
            else:
                i += 1
        print(f"Fragmentação externa: {external_fragments} buracos menores que {min_process_size} blocos")
        return external_fragments
