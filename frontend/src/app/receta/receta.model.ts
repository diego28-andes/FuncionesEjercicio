export interface Receta {
  id: number;
  nombre: string;
  descripcion: string;
  tiempo_preparacion: number;
  dificultad: string;
  porciones: number;
  ingrediente_id: number;
  ingrediente?: Ingrediente;
}

export interface Ingrediente {
  id: number;
  nombre: string;
  tipo: string;
  unidad_medida: string;
  disponible: boolean;
}