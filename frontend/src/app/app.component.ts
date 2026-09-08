import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RecetaService } from './receta/receta.service';
import { IngredienteService } from './ingrediente/ingrediente.service';
import { Receta } from './receta/receta.model';
import { Ingrediente } from './ingrediente/ingrediente.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  vistaActual = 'principal';
  recetas: Receta[] = [];
  ingredientes: Ingrediente[] = [];
  recetaSeleccionada: Receta | null = null;
  ingredienteSeleccionado: Ingrediente | null = null;
  modoEdicion = false;
  reporteData: any = null;
  mensaje = '';
  tipoMensaje = '';

  nuevaReceta = {
    nombre: '',
    descripcion: '',
    tiempo_preparacion: 30,
    dificultad: 'Fácil',
    porciones: 4,
    ingrediente_id: 1
  };

  nuevoIngrediente = {
    nombre: '',
    tipo: '',
    unidad_medida: 'gramos',
    disponible: true
  };

  constructor(
    private recetaService: RecetaService,
    private ingredienteService: IngredienteService,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.cargarRecetas();
    this.cargarIngredientes();
  }

  mostrarVista(vista: string) {
    this.vistaActual = vista;
    if (vista !== 'agregar-receta' && vista !== 'agregar-ingrediente') {
      this.modoEdicion = false;
      this.recetaSeleccionada = null;
      this.ingredienteSeleccionado = null;
      this.resetearFormularios();
    }
    if (vista === 'reporte') {
      this.cargarReporte();
    }
  }

  resetearFormularios() {
    this.nuevaReceta = {
      nombre: '',
      descripcion: '',
      tiempo_preparacion: 30,
      dificultad: 'Fácil',
      porciones: 4,
      ingrediente_id: 1
    };
    this.nuevoIngrediente = {
      nombre: '',
      tipo: '',
      unidad_medida: 'gramos',
      disponible: true
    };
  }

  cargarRecetas() {
    this.recetaService.obtenerRecetas().subscribe(
      data => this.recetas = data,
      error => this.mostrarMensaje('Error al cargar recetas', 'danger')
    );
  }

  cargarIngredientes() {
    this.ingredienteService.obtenerIngredientes().subscribe(
      data => this.ingredientes = data,
      error => this.mostrarMensaje('Error al cargar ingredientes', 'danger')
    );
  }

  cargarReporte() {
    this.http.get('http://localhost:5001/api/reportes/ingredientes').subscribe(
      data => this.reporteData = data,
      error => this.mostrarMensaje('Error cargando reporte', 'danger')
    );
  }

  crearReceta() {
    this.recetaService.crearReceta(this.nuevaReceta).subscribe(
      response => {
        this.cargarRecetas();
        this.mostrarVista('principal');
        this.mostrarMensaje('Receta creada exitosamente', 'success');
      },
      error => this.mostrarMensaje('Error al crear la receta', 'danger')
    );
  }

  editarReceta(receta: Receta) {
    this.recetaSeleccionada = { ...receta };
    this.nuevaReceta = {
      nombre: receta.nombre,
      descripcion: receta.descripcion,
      tiempo_preparacion: receta.tiempo_preparacion,
      dificultad: receta.dificultad,
      porciones: receta.porciones,
      ingrediente_id: receta.ingrediente_id
    };
    this.modoEdicion = true;
    this.mostrarVista('agregar-receta');
  }

  actualizarReceta() {
    if (this.recetaSeleccionada) {
      this.recetaService.actualizarReceta(this.recetaSeleccionada.id, this.nuevaReceta).subscribe(
        response => {
          this.cargarRecetas();
          this.mostrarVista('principal');
          this.mostrarMensaje('Receta actualizada exitosamente', 'success');
        },
        error => this.mostrarMensaje('Error al actualizar la receta', 'danger')
      );
    }
  }

  eliminarReceta(receta: Receta) {
    if (confirm(`¿Está seguro de eliminar la receta "${receta.nombre}"?`)) {
      this.recetaService.eliminarReceta(receta.id).subscribe(
        response => {
          this.cargarRecetas();
          this.mostrarMensaje('Receta eliminada exitosamente', 'success');
        },
        error => this.mostrarMensaje('Error al eliminar la receta', 'danger')
      );
    }
  }

  verDetallesReceta(receta: Receta) {
    this.recetaSeleccionada = receta;
    this.vistaActual = 'detalles-receta';
  }

  crearIngrediente() {
    this.ingredienteService.crearIngrediente(this.nuevoIngrediente).subscribe(
      response => {
        this.cargarIngredientes();
        this.mostrarVista('ingredientes');
        this.mostrarMensaje('Ingrediente creado exitosamente', 'success');
      },
      error => this.mostrarMensaje('Error al crear el ingrediente', 'danger')
    );
  }

  editarIngrediente(ingrediente: Ingrediente) {
    this.ingredienteSeleccionado = { ...ingrediente };
    this.nuevoIngrediente = {
      nombre: ingrediente.nombre,
      tipo: ingrediente.tipo,
      unidad_medida: ingrediente.unidad_medida,
      disponible: ingrediente.disponible
    };
    this.modoEdicion = true;
    this.mostrarVista('agregar-ingrediente');
  }

  actualizarIngrediente() {
    if (this.ingredienteSeleccionado) {
      this.ingredienteService.actualizarIngrediente(this.ingredienteSeleccionado.id, this.nuevoIngrediente).subscribe(
        response => {
          this.cargarIngredientes();
          this.mostrarVista('ingredientes');
          this.mostrarMensaje('Ingrediente actualizado exitosamente', 'success');
        },
        error => this.mostrarMensaje('Error al actualizar el ingrediente', 'danger')
      );
    }
  }

  eliminarIngrediente(ingrediente: Ingrediente) {
    if (confirm(`¿Está seguro de eliminar el ingrediente "${ingrediente.nombre}"?`)) {
      this.ingredienteService.eliminarIngrediente(ingrediente.id).subscribe(
        response => {
          this.cargarIngredientes();
          this.mostrarMensaje('Ingrediente eliminado exitosamente', 'success');
        },
        error => this.mostrarMensaje('Error al eliminar el ingrediente', 'danger')
      );
    }
  }

  mostrarMensaje(texto: string, tipo: string) {
    this.mensaje = texto;
    this.tipoMensaje = tipo;
    setTimeout(() => {
      this.mensaje = '';
      this.tipoMensaje = '';
    }, 3000);
  }

  obtenerNombreIngrediente(ingredienteId: number): string {
    const ingrediente = this.ingredientes.find(i => i.id === ingredienteId);
    return ingrediente ? ingrediente.nombre : 'Sin ingrediente';
  }

  obtenerClaseDificultad(dificultad: string): string {
    switch(dificultad) {
      case 'Fácil': return 'difficulty-easy';
      case 'Medio': return 'difficulty-medium';
      case 'Difícil': return 'difficulty-hard';
      default: return '';
    }
  }
}