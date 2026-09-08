export interface Ingrediente {
  id: number;
  nombre: string;
  tipo: string;
  unidad_medida: string;
  disponible: boolean;
  cantidad_recetas?: number;
}