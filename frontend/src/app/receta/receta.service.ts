import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Receta } from './receta.model';

@Injectable({
  providedIn: 'root'
})
export class RecetaService {
  private apiUrl = 'http://localhost:5001/api/recetas';

  constructor(private http: HttpClient) { }

  obtenerRecetas(): Observable<Receta[]> {
    return this.http.get<Receta[]>(this.apiUrl);
  }

  obtenerReceta(id: number): Observable<Receta> {
    return this.http.get<Receta>(`${this.apiUrl}/${id}`);
  }

  crearReceta(receta: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, receta);
  }

  actualizarReceta(id: number, receta: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, receta);
  }

  eliminarReceta(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}