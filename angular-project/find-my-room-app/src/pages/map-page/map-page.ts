import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { APIService } from '../../services/api-service';

interface Node {
  id: string;
  label: string;
  type: string;
}

@Component({
  selector: 'app-map-page',
  imports: [CommonModule, FormsModule],
  templateUrl: './map-page.html',
  styleUrl: './map-page.css',
})
export class MapPage implements OnInit {
  nodes: Node[] = [];
  filteredNodesFrom: Node[] = [];
  filteredNodesTo: Node[] = [];
  
  searchFrom: string = '';
  searchTo: string = '';
  
  selectedFrom: Node | null = null;
  selectedTo: Node | null = null;
  
  showDropdownFrom: boolean = false;
  showDropdownTo: boolean = false;

  items = [
    { direction: 'Turn right at the next intersection', imgSrc: 'assets/turn-right.png' },
    { direction: 'Walk straight for 200 meters', imgSrc: 'assets/walk-straight.png' },
    { direction: 'Your destination will be on the left', imgSrc: 'assets/destination-left.png' }
  ];

  constructor(private apiService: APIService) {}

  ngOnInit(): void {
    // Cargar todos los nodos al iniciar
    // this.apiService.getNodes().subscribe({
    //   next: (data: any) => {
    //     this.nodes = data;
    //     this.filteredNodesFrom = data;
    //     this.filteredNodesTo = data;
    //   },
    //   error: (error) => {
    //     console.error('Error loading nodes:', error);
    //   }
    // });
  }

  onSearchFromChange(): void {
    this.showDropdownFrom = true;
    this.filteredNodesFrom = this.nodes.filter(node =>
      node.label.toLowerCase().includes(this.searchFrom.toLowerCase()) ||
      node.id.toLowerCase().includes(this.searchFrom.toLowerCase())
    );
  }

  onSearchToChange(): void {
    this.showDropdownTo = true;
    this.filteredNodesTo = this.nodes.filter(node =>
      node.label.toLowerCase().includes(this.searchTo.toLowerCase()) ||
      node.id.toLowerCase().includes(this.searchTo.toLowerCase())
    );
  }

  selectNodeFrom(node: Node): void {
    this.selectedFrom = node;
    this.searchFrom = node.label;
    this.showDropdownFrom = false;
  }

  selectNodeTo(node: Node): void {
    this.selectedTo = node;
    this.searchTo = node.label;
    this.showDropdownTo = false;
  }

  findRoute(): void {
    if (!this.selectedFrom || !this.selectedTo) {
      alert('Please select both origin and destination');
      return;
    }

    this.apiService.findRoute(this.selectedFrom.id, this.selectedTo.id).subscribe({
      next: (response: any) => {
        console.log('Route found:', response);
        this.items = response.instructions.map((inst: any) => ({
          direction: inst.instruction,
          imgSrc: ''
        }));
      },
      error: (error) => {
        console.error('Error finding route:', error);
        alert('No route found');
      }
    });
  }

  printDirections(): void {
    this.apiService.getNodes().subscribe({
      next: (data) => {
        const jsonString = JSON.stringify(data, null, 2);
        console.log("Nodes as string: " + jsonString);
      },
      error: (error) => {
        console.error("Error fetching the nodes from the backend");
      }
    });
  }

  getIcon(direction: string): string {
    if (direction.includes('right')) return 'turn_right';
    if (direction.includes('left')) return 'turn_left';
    if (direction.includes("straight")) return 'straight';
    return "location_on";
  }
}
