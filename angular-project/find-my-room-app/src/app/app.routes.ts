import { Routes } from '@angular/router';
import { LandingPage } from '../pages/landing-page/landing-page';
import { MapPage } from '../pages/map-page/map-page';

export const routes: Routes = [
    { path: '', component: LandingPage },
    { path: 'map', component: MapPage}
];
