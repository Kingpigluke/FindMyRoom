import { Component } from '@angular/core';
import { APIService } from '../../services/api-service';

@Component({
  selector: 'app-map-page',
  imports: [],
  templateUrl: './map-page.html',
  styleUrl: './map-page.css',
})
export class MapPage {

  constructor(private apiService: APIService){}
  items = [
    { direction: 'Turn right at the next intersection', imgSrc: 'assets/turn-right.png' },
    { direction: 'Walk straight for 200 meters', imgSrc: 'assets/walk-straight.png' },
    { direction: 'Your destination will be on the left', imgSrc: 'assets/destination-left.png' }
  ];

  printDirections(): void
  {
    this.apiService.getNodes().subscribe({
      next: (data) => {
        const jsonString = JSON.stringify(data, null, 2);
        console.log("Nodes as string: " + jsonString);
      },
      error: (error) => {
        console.error("Error fetching the nodes from the backend");
      }
    })
  }

  getIcon(direction:string):string 
  {
    if(direction.includes('right')) return 'turn_right';
    if(direction.includes('left')) return 'turn_left';
    if(direction.includes("straight")) return 'straight';
    return "location_on";
  }
}
