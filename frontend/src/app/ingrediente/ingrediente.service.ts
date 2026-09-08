import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ingrediente } from './ingrediente.model';

@Injectable({
  providedIn: 'root'
})
export class IngredienteService {
  private apiUrl = 'http://localhost:5001/api/ingredientes';

  constructor(private http: HttpClient) { }

  obtenerIngredientes(): Observable<Ingrediente[]> {
    return this.http.get<Ingrediente[]>(this.apiUrl);
  }

  obtenerIngrediente(id: number): Observable<Ingrediente> {
    return this.http.get<Ingrediente>(`${this.apiUrl}/${id}`);
  }

  crearIngrediente(ingrediente: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, ingrediente);
  }

  actualizarIngrediente(id: number, ingrediente: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, ingrediente);
  }

  eliminarIngrediente(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}