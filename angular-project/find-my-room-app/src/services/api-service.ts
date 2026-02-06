import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class APIService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // Obtener todos los nodos
  getNodes() {
    return this.http.get(`${this.apiUrl}/nodes`);
  }

  // Calcular ruta
  findRoute(start: string, end: string) {
    return this.http.post(`${this.apiUrl}/route`, { start, end });
  }
}
