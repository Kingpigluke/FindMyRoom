import { Component } from '@angular/core';

@Component({
  selector: 'app-map-page',
  imports: [],
  templateUrl: './map-page.html',
  styleUrl: './map-page.css',
})
export class MapPage {
  items = [
    { direction: 'Turn right at the next intersection', imgSrc: 'assets/turn-right.png' },
    { direction: 'Walk straight for 200 meters', imgSrc: 'assets/walk-straight.png' },
    { direction: 'Your destination will be on the left', imgSrc: 'assets/destination-left.png' }
  ];

  getIcon(direction:string):string 
  {
    if(direction.includes('right')) return 'turn_right';
    if(direction.includes('left')) return 'turn_left';
    if(direction.includes("straight")) return 'straight';
    return "location_on";
  }
}
