import tkinter as tk
from tkinter import ttk, messagebox
import heapq

class Router:
    def __init__(self, router_id, x, y):
        self.router_id = router_id
        self.neighbors = {}
        self.routing_table = {}
        self.x = x
        self.y = y
    
    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost
    
    def dijkstra(self, all_routers):
        self.routing_table = {}
        distances = {self.router_id: 0}
        parent = {self.router_id: None}
        visited = set()
        heap = [(0, self.router_id)]
        
        while heap:
            current_dist, current_id = heapq.heappop(heap)
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            if current_id in all_routers:
                router = all_routers[current_id]
                for neighbor_id, cost in router.neighbors.items():
                    if neighbor_id not in visited:
                        new_dist = distances[current_id] + cost
                        if neighbor_id not in distances or new_dist < distances[neighbor_id]:
                            distances[neighbor_id] = new_dist
                            parent[neighbor_id] = current_id
                            heapq.heappush(heap, (new_dist, neighbor_id))
        
        for dest_id in all_routers.keys():
            if dest_id != self.router_id and dest_id in distances:
                self.routing_table[dest_id] = distances[dest_id]
        
        return parent

class OSPFGui:
    def __init__(self, root):
        self.root = root
        self.root.title("OSPF Protocol Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a1a")
        self.routers = {}
        self.links = []
        self.canvas_width = 600
        self.canvas_height = 500
        self.highlighted_path = []
        self.parent_map = {}
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabel', background='#1a1a1a', foreground='#ffffff')
        style.configure('TLabelframe', background='#1a1a1a', foreground='#ffffff')
        style.configure('TLabelframe.Label', background='#1a1a1a', foreground='#64b5f6')
        style.configure('TButton', background='#2196F3', foreground='#ffffff')
        style.map('TButton', background=[('active', '#1976D2')])
        style.configure('TEntry', fieldbackground='#2a2a2a', foreground='#ffffff')
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        canvas_label = ttk.Label(left_frame, text="Network Topology", font=("Arial", 14, "bold"), foreground="#64b5f6")
        canvas_label.pack()
        
        self.canvas = tk.Canvas(left_frame, width=self.canvas_width, height=self.canvas_height, 
                                bg='#0a0a0a', highlightthickness=2, highlightbackground='#404040')
        self.canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_frame, text="Configuration", font=("Arial", 14, "bold"), foreground="#64b5f6").pack()
        
        router_frame = ttk.LabelFrame(right_frame, text="Add Router", padding=10)
        router_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(router_frame, text="Router ID:", foreground="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.router_id_var = tk.StringVar()
        ttk.Entry(router_frame, textvariable=self.router_id_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(router_frame, text="Add Router", command=self.add_router).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
        
        link_frame = ttk.LabelFrame(right_frame, text="Add Link", padding=10)
        link_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(link_frame, text="Router 1:", foreground="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.r1_var = tk.StringVar()
        ttk.Entry(link_frame, textvariable=self.r1_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(link_frame, text="Router 2:", foreground="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.r2_var = tk.StringVar()
        ttk.Entry(link_frame, textvariable=self.r2_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(link_frame, text="Cost:", foreground="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.cost_var = tk.StringVar()
        ttk.Entry(link_frame, textvariable=self.cost_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(link_frame, text="Add Link", command=self.add_link).grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        run_button = ttk.Button(button_frame, text="▶ Run OSPF", command=self.run_ospf)
        run_button.pack(fill=tk.X, pady=5, ipady=8)
        
        clear_button = ttk.Button(button_frame, text="🗑 Clear All", command=self.clear_all)
        clear_button.pack(fill=tk.X, pady=5, ipady=8)
        
        path_frame = ttk.LabelFrame(right_frame, text="Find Path", padding=10)
        path_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(path_frame, text="Start Router:", foreground="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.start_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(path_frame, text="Destination:", foreground="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dest_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.dest_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(path_frame, text="Show Path", command=self.show_path).grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        ttk.Label(right_frame, text="Routing Tables", font=("Arial", 12, "bold"), foreground="#64b5f6").pack(pady=(15, 5))
        
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output_text = tk.Text(table_frame, height=15, width=35, font=("Courier", 9),
                                    bg='#0a0a0a', fg='#64b5f6', insertbackground='#64b5f6',
                                    yscrollcommand=scrollbar.set)
        self.output_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=self.output_text.yview)
    
    def add_router(self):
        try:
            router_id = int(self.router_id_var.get())
            if router_id in self.routers:
                messagebox.showerror("Error", "Router already exists")
                return
            
            x = 50 + (len(self.routers) % 3) * 150
            y = 50 + (len(self.routers) // 3) * 150
            
            self.routers[router_id] = Router(router_id, x, y)
            messagebox.showinfo("Success", f"Router {router_id} added")
            self.router_id_var.set("")
            self.draw_topology()
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid router ID")
    
    def add_link(self):
        try:
            r1 = int(self.r1_var.get())
            r2 = int(self.r2_var.get())
            cost = int(self.cost_var.get())
            
            if r1 not in self.routers or r2 not in self.routers:
                messagebox.showerror("Error", "One or both routers don't exist")
                return
            
            if r1 == r2:
                messagebox.showerror("Error", "Cannot link a router to itself")
                return
            
            self.routers[r1].add_neighbor(r2, cost)
            self.routers[r2].add_neighbor(r1, cost)
            self.links.append((r1, r2, cost))
            
            messagebox.showinfo("Success", f"Link added: {r1} <-> {r2} (cost {cost})")
            self.r1_var.set("")
            self.r2_var.set("")
            self.cost_var.set("")
            self.draw_topology()
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
    
    def run_ospf(self):
        if not self.routers:
            messagebox.showerror("Error", "No routers configured")
            return
        
        for router in self.routers.values():
            parent = router.dijkstra(self.routers)
            self.parent_map[router.router_id] = parent
        
        self.highlighted_path = []
        self.draw_topology()
        self.update_display()
    
    def get_path(self, start, dest):
        if start not in self.parent_map or dest not in self.routers:
            return None
        
        path = []
        current = dest
        parent_map = self.parent_map[start]
        
        while current is not None:
            path.append(current)
            current = parent_map.get(current)
        
        path.reverse()
        
        if path[0] != start:
            return None
        
        return path
    
    def show_path(self):
        try:
            start = int(self.start_var.get())
            dest = int(self.dest_var.get())
            
            if start not in self.routers or dest not in self.routers:
                messagebox.showerror("Error", "Start or destination router doesn't exist")
                return
            
            if start == dest:
                messagebox.showerror("Error", "Start and destination must be different")
                return
            
            if not self.parent_map or start not in self.parent_map:
                messagebox.showerror("Error", "Run OSPF first")
                return
            
            path = self.get_path(start, dest)
            if path is None or len(path) < 2:
                messagebox.showerror("Error", "No path found")
                return
            
            self.highlighted_path = path
            self.draw_topology()
            
            path_str = " → ".join(str(r) for r in path)
            total_cost = self.routers[start].routing_table.get(dest, "N/A")
            messagebox.showinfo("Path Found", f"Path: {path_str}\nTotal Cost: {total_cost}")
        except ValueError:
            messagebox.showerror("Error", "Invalid router ID")
    
    def clear_all(self):
        self.routers = {}
        self.links = []
        self.parent_map = {}
        self.highlighted_path = []
        self.output_text.delete(1.0, tk.END)
        self.draw_topology()
        messagebox.showinfo("Cleared", "All routers and links cleared")
    
    def draw_topology(self):
        self.canvas.delete("all")
        
        for r1, r2, cost in self.links:
            if r1 in self.routers and r2 in self.routers:
                router1 = self.routers[r1]
                router2 = self.routers[r2]
                
                is_in_path = False
                if len(self.highlighted_path) > 1:
                    for i in range(len(self.highlighted_path) - 1):
                        if (self.highlighted_path[i] == r1 and self.highlighted_path[i+1] == r2) or \
                           (self.highlighted_path[i] == r2 and self.highlighted_path[i+1] == r1):
                            is_in_path = True
                            break
                
                line_color = '#00ff00' if is_in_path else '#404040'
                line_width = 4 if is_in_path else 2
                
                self.canvas.create_line(router1.x, router1.y, router2.x, router2.y, 
                                      fill=line_color, width=line_width)
                
                mid_x = (router1.x + router2.x) / 2
                mid_y = (router1.y + router2.y) / 2
                self.canvas.create_text(mid_x, mid_y - 10, text=str(cost), 
                                      fill='#fbbf24', font=("Arial", 10, "bold"))
        
        for router in self.routers.values():
            is_in_path = router.router_id in self.highlighted_path
            node_color = '#00ff00' if is_in_path else '#2196F3'
            outline_color = '#00ff00' if is_in_path else '#64b5f6'
            
            self.canvas.create_oval(router.x - 15, router.y - 15, 
                                  router.x + 15, router.y + 15, 
                                  fill=node_color, outline=outline_color, width=2)
            
            self.canvas.create_text(router.x, router.y, text=str(router.router_id), 
                                  fill='#ffffff', font=("Arial", 12, "bold"))
    
    def update_display(self):
        self.output_text.delete(1.0, tk.END)
        
        if not self.routers:
            self.output_text.insert(tk.END, "No routers configured")
            return
        
        self.output_text.insert(tk.END, "OSPF ROUTING TABLES\n")
        self.output_text.insert(tk.END, "=" * 32 + "\n\n")
        
        for router_id in sorted(self.routers.keys()):
            router = self.routers[router_id]
            self.output_text.insert(tk.END, f"Router {router_id}:\n")
            self.output_text.insert(tk.END, "-" * 32 + "\n")
            
            if not router.routing_table:
                self.output_text.insert(tk.END, "  No routes available\n\n")
            else:
                for dest in sorted(router.routing_table.keys()):
                    distance = router.routing_table[dest]
                    self.output_text.insert(tk.END, f"  Dest {dest}: distance {distance}\n")
                self.output_text.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    gui = OSPFGui(root)
    root.mainloop()