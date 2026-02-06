import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from biblioteca.models import Libro, Resena, Prestamo, ListaDeseos
from datetime import date, timedelta
import random

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Puebla la base de datos con libros de ejemplo, usuarios y datos de prueba'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creando datos de ejemplo...'))

        # ====== USUARIOS ======
        admin_user, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Administrador',
                'last_name': 'Bibliandria',
                'email': 'admin@bibliandria.es',
                'rol': 'admin',
                'biblioteca_publica': True,
            }
        )
        # Siempre asegurar que el admin tenga contraseña y permisos correctos
        admin_user.set_password('admin1234')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.rol = 'admin'
        admin_user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'  Usuario admin creado (admin / admin1234)'))
        else:
            self.stdout.write(self.style.SUCCESS(f'  Usuario admin actualizado (admin / admin1234)'))

        biblio1, created = Usuario.objects.get_or_create(
            username='maria_lectora',
            defaults={
                'first_name': 'María',
                'last_name': 'García López',
                'email': 'maria@bibliandria.es',
                'rol': 'bibliotecario',
                'biblioteca_publica': True,
            }
        )
        if created:
            biblio1.set_password('maria1234')
            biblio1.save()
            self.stdout.write(self.style.SUCCESS(f'  Usuario maria_lectora creado (maria_lectora / maria1234)'))

        biblio2, created = Usuario.objects.get_or_create(
            username='carlos_libros',
            defaults={
                'first_name': 'Carlos',
                'last_name': 'Martínez Ruiz',
                'email': 'carlos@bibliandria.es',
                'rol': 'bibliotecario',
                'biblioteca_publica': True,
            }
        )
        if created:
            biblio2.set_password('carlos1234')
            biblio2.save()
            self.stdout.write(self.style.SUCCESS(f'  Usuario carlos_libros creado (carlos_libros / carlos1234)'))

        biblio3, created = Usuario.objects.get_or_create(
            username='ana_biblioteca',
            defaults={
                'first_name': 'Ana',
                'last_name': 'Fernández Pérez',
                'email': 'ana@bibliandria.es',
                'rol': 'bibliotecario',
                'biblioteca_publica': False,
            }
        )
        if created:
            biblio3.set_password('ana12345')
            biblio3.save()
            self.stdout.write(self.style.SUCCESS(f'  Usuario ana_biblioteca creado (ana_biblioteca / ana12345)'))

        visitante, created = Usuario.objects.get_or_create(
            username='pedro_visitante',
            defaults={
                'first_name': 'Pedro',
                'last_name': 'Sánchez Gómez',
                'email': 'pedro@bibliandria.es',
                'rol': 'visitante',
                'biblioteca_publica': False,
            }
        )
        if created:
            visitante.set_password('pedro1234')
            visitante.save()
            self.stdout.write(self.style.SUCCESS(f'  Usuario pedro_visitante creado (pedro_visitante / pedro1234)'))

        # ====== LIBROS ======
        libros_data = [
            # --- Biblioteca de María ---
            {
                'propietario': biblio1,
                'titulo': 'Cien años de soledad',
                'autor': 'Gabriel García Márquez',
                'isbn': '9788497592208',
                'editorial': 'Cátedra',
                'año_publicacion': 1967,
                'descripcion': 'La historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo. Una obra maestra del realismo mágico que explora temas de soledad, amor y el destino inexorable.',
                'numero_paginas': 471,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio1,
                'titulo': 'Don Quijote de la Mancha',
                'autor': 'Miguel de Cervantes',
                'isbn': '9788491050087',
                'editorial': 'Real Academia Española',
                'año_publicacion': 1605,
                'descripcion': 'Las aventuras del ingenioso hidalgo Don Quijote y su fiel escudero Sancho Panza. La primera novela moderna de la literatura universal.',
                'numero_paginas': 1250,
                'estado': 'como_nuevo',
                'formato': 'tapa_dura',
            },
            {
                'propietario': biblio1,
                'titulo': 'La casa de los espíritus',
                'autor': 'Isabel Allende',
                'isbn': '9788401352812',
                'editorial': 'Plaza & Janés',
                'año_publicacion': 1982,
                'descripcion': 'La saga de la familia Trueba, que abarca cuatro generaciones y refleja los cambios políticos y sociales de un país sudamericano.',
                'numero_paginas': 448,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio1,
                'titulo': 'El amor en los tiempos del cólera',
                'autor': 'Gabriel García Márquez',
                'isbn': '9788497592451',
                'editorial': 'Mondadori',
                'año_publicacion': 1985,
                'descripcion': 'Una historia de amor que dura más de medio siglo, ambientada en una ciudad caribeña. Florentino Ariza espera pacientemente por el amor de Fermina Daza.',
                'numero_paginas': 368,
                'estado': 'nuevo',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio1,
                'titulo': '1984',
                'autor': 'George Orwell',
                'isbn': '9788499890944',
                'editorial': 'Debolsillo',
                'año_publicacion': 1949,
                'descripcion': 'Una novela distópica que describe un futuro totalitario donde el Gran Hermano vigila a todos. Una obra fundamental sobre la libertad y el control social.',
                'numero_paginas': 326,
                'estado': 'como_nuevo',
                'formato': 'bolsillo',
            },
            {
                'propietario': biblio1,
                'titulo': 'Rayuela',
                'autor': 'Julio Cortázar',
                'isbn': '9788437604572',
                'editorial': 'Cátedra',
                'año_publicacion': 1963,
                'descripcion': 'Una contranovela revolucionaria que puede leerse de múltiples maneras. La historia de Horacio Oliveira entre París y Buenos Aires.',
                'numero_paginas': 736,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio1,
                'titulo': 'El Principito',
                'autor': 'Antoine de Saint-Exupéry',
                'isbn': '9788498381498',
                'editorial': 'Salamandra',
                'año_publicacion': 1943,
                'descripcion': 'Un piloto perdido en el desierto del Sahara se encuentra con un pequeño príncipe llegado de otro planeta. Una fábula poética sobre la amistad, el amor y la pérdida.',
                'numero_paginas': 96,
                'estado': 'nuevo',
                'formato': 'tapa_dura',
            },
            {
                'propietario': biblio1,
                'titulo': 'Sapiens: De animales a dioses',
                'autor': 'Yuval Noah Harari',
                'isbn': '9788499926223',
                'editorial': 'Debate',
                'año_publicacion': 2011,
                'descripcion': 'Un recorrido fascinante por la historia de la humanidad, desde los primeros humanos hasta la actualidad. Cómo hemos llegado a dominar el planeta.',
                'numero_paginas': 496,
                'estado': 'como_nuevo',
                'formato': 'tapa_blanda',
            },

            # --- Biblioteca de Carlos ---
            {
                'propietario': biblio2,
                'titulo': 'El nombre de la rosa',
                'autor': 'Umberto Eco',
                'isbn': '9788497592536',
                'editorial': 'Debolsillo',
                'año_publicacion': 1980,
                'descripcion': 'Una novela histórica ambientada en una abadía benedictina del siglo XIV donde ocurren misteriosos asesinatos. Fray Guillermo de Baskerville investiga los crímenes.',
                'numero_paginas': 640,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio2,
                'titulo': 'Crimen y castigo',
                'autor': 'Fiódor Dostoyevski',
                'isbn': '9788420674278',
                'editorial': 'Alianza Editorial',
                'año_publicacion': 1866,
                'descripcion': 'La historia de Raskólnikov, un estudiante que comete un asesinato y se enfrenta a las consecuencias morales y psicológicas de su acto.',
                'numero_paginas': 672,
                'estado': 'usado_aceptable',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio2,
                'titulo': 'Tokio Blues (Norwegian Wood)',
                'autor': 'Haruki Murakami',
                'isbn': '9788483835043',
                'editorial': 'Tusquets',
                'año_publicacion': 1987,
                'descripcion': 'Una novela nostálgica sobre amor, pérdida y crecimiento personal en el Tokio de los años sesenta. La historia de Toru Watanabe y sus relaciones.',
                'numero_paginas': 384,
                'estado': 'como_nuevo',
                'formato': 'bolsillo',
            },
            {
                'propietario': biblio2,
                'titulo': 'El señor de los anillos: La comunidad del anillo',
                'autor': 'J.R.R. Tolkien',
                'isbn': '9788445073735',
                'editorial': 'Minotauro',
                'año_publicacion': 1954,
                'descripcion': 'El comienzo de la épica aventura de Frodo Bolsón para destruir el Anillo Único. Una obra que definió el género de la fantasía moderna.',
                'numero_paginas': 576,
                'estado': 'usado_bueno',
                'formato': 'tapa_dura',
            },
            {
                'propietario': biblio2,
                'titulo': 'Fahrenheit 451',
                'autor': 'Ray Bradbury',
                'isbn': '9788445076439',
                'editorial': 'Minotauro',
                'año_publicacion': 1953,
                'descripcion': 'En un futuro donde los libros están prohibidos, el bombero Guy Montag se rebela contra el sistema. Una reflexión sobre la censura y el valor de la literatura.',
                'numero_paginas': 176,
                'estado': 'nuevo',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio2,
                'titulo': 'El código Da Vinci',
                'autor': 'Dan Brown',
                'isbn': '9788408176008',
                'editorial': 'Planeta',
                'año_publicacion': 2003,
                'descripcion': 'Robert Langdon investiga un misterioso asesinato en el Louvre que lo lleva a descubrir un secreto que la Iglesia ha guardado durante siglos.',
                'numero_paginas': 560,
                'estado': 'usado_bueno',
                'formato': 'bolsillo',
            },
            {
                'propietario': biblio2,
                'titulo': 'Breve historia del tiempo',
                'autor': 'Stephen Hawking',
                'isbn': '9788498921540',
                'editorial': 'Crítica',
                'año_publicacion': 1988,
                'descripcion': 'Una explicación accesible de los conceptos fundamentales de la física moderna: el Big Bang, los agujeros negros, la teoría de cuerdas y el tiempo.',
                'numero_paginas': 256,
                'estado': 'como_nuevo',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio2,
                'titulo': 'Dune',
                'autor': 'Frank Herbert',
                'isbn': '9788497596824',
                'editorial': 'Debolsillo',
                'año_publicacion': 1965,
                'descripcion': 'En el desértico planeta Arrakis, Paul Atreides lucha por el control de la especia más valiosa del universo. Ciencia ficción épica sobre política, religión y ecología.',
                'numero_paginas': 784,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },

            # --- Biblioteca de Ana ---
            {
                'propietario': biblio3,
                'titulo': 'Orgullo y prejuicio',
                'autor': 'Jane Austen',
                'isbn': '9788491050209',
                'editorial': 'Alianza Editorial',
                'año_publicacion': 1813,
                'descripcion': 'La historia de Elizabeth Bennet y el señor Darcy. Una novela sobre el amor, las clases sociales y los malentendidos en la Inglaterra del siglo XIX.',
                'numero_paginas': 432,
                'estado': 'como_nuevo',
                'formato': 'tapa_dura',
            },
            {
                'propietario': biblio3,
                'titulo': 'Matar a un ruiseñor',
                'autor': 'Harper Lee',
                'isbn': '9788466636438',
                'editorial': 'HarperCollins',
                'año_publicacion': 1960,
                'descripcion': 'Scout Finch narra la historia de su padre, el abogado Atticus Finch, quien defiende a un hombre negro acusado injustamente en el sur de Estados Unidos.',
                'numero_paginas': 352,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio3,
                'titulo': 'La sombra del viento',
                'autor': 'Carlos Ruiz Zafón',
                'isbn': '9788408163435',
                'editorial': 'Planeta',
                'año_publicacion': 2001,
                'descripcion': 'Daniel Sempere descubre un libro misterioso en el Cementerio de los Libros Olvidados y se embarca en una aventura por la Barcelona de posguerra.',
                'numero_paginas': 576,
                'estado': 'nuevo',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': biblio3,
                'titulo': 'Crónica de una muerte anunciada',
                'autor': 'Gabriel García Márquez',
                'isbn': '9788497592437',
                'editorial': 'Mondadori',
                'año_publicacion': 1981,
                'descripcion': 'La reconstrucción periodística del asesinato de Santiago Nasar. Todos en el pueblo sabían que iba a morir, pero nadie hizo nada para impedirlo.',
                'numero_paginas': 138,
                'estado': 'usado_bueno',
                'formato': 'bolsillo',
            },
            {
                'propietario': biblio3,
                'titulo': 'El alquimista',
                'autor': 'Paulo Coelho',
                'isbn': '9788408045083',
                'editorial': 'Planeta',
                'año_publicacion': 1988,
                'descripcion': 'Santiago, un joven pastor andaluz, viaja al desierto del Sahara en busca de un tesoro. Una fábula sobre seguir los sueños y escuchar al corazón.',
                'numero_paginas': 208,
                'estado': 'como_nuevo',
                'formato': 'tapa_blanda',
            },

            # --- Biblioteca del Admin ---
            {
                'propietario': admin_user,
                'titulo': 'Clean Code',
                'autor': 'Robert C. Martin',
                'isbn': '9780132350884',
                'editorial': 'Prentice Hall',
                'año_publicacion': 2008,
                'descripcion': 'Una guía para escribir código limpio y mantenible. Principios ágiles, patrones y prácticas para desarrolladores de software profesionales.',
                'numero_paginas': 464,
                'estado': 'como_nuevo',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': admin_user,
                'titulo': 'El pragmatic programmer',
                'autor': 'Andrew Hunt y David Thomas',
                'isbn': '9780135957059',
                'editorial': 'Addison-Wesley',
                'año_publicacion': 1999,
                'descripcion': 'Consejos prácticos para desarrolladores de software. Desde la gestión de la carrera profesional hasta técnicas de codificación y depuración.',
                'numero_paginas': 352,
                'estado': 'usado_bueno',
                'formato': 'tapa_blanda',
            },
            {
                'propietario': admin_user,
                'titulo': 'Designing Data-Intensive Applications',
                'autor': 'Martin Kleppmann',
                'isbn': '9781449373320',
                'editorial': "O'Reilly Media",
                'año_publicacion': 2017,
                'descripcion': 'Una guía completa sobre los principios y prácticas de ingeniería de datos. Bases de datos distribuidas, procesamiento de streams y arquitectura de sistemas.',
                'numero_paginas': 616,
                'estado': 'nuevo',
                'formato': 'tapa_blanda',
            },
        ]

        libros_creados = []
        for libro_data in libros_data:
            libro, created = Libro.objects.get_or_create(
                titulo=libro_data['titulo'],
                propietario=libro_data['propietario'],
                defaults=libro_data
            )
            libros_creados.append(libro)
            if created:
                self.stdout.write(f'  Libro creado: {libro.titulo} ({libro.propietario.username})')

        # ====== RESEÑAS ======
        resenas_data = [
            {
                'libro_titulo': 'Cien años de soledad',
                'propietario': biblio1,
                'puntuacion': 5,
                'comentario': 'Una obra maestra absoluta. García Márquez crea un universo mágico que atrapa desde la primera página. La prosa es hipnótica y los personajes son inolvidables. Una de las mejores novelas que he leído jamás.',
                'fecha_lectura': date(2024, 6, 15),
            },
            {
                'libro_titulo': 'Don Quijote de la Mancha',
                'propietario': biblio1,
                'puntuacion': 5,
                'comentario': 'La gran novela de la literatura española. Cervantes fue un genio adelantado a su época. La relación entre Don Quijote y Sancho es entrañable. Lectura obligatoria.',
                'fecha_lectura': date(2024, 3, 20),
            },
            {
                'libro_titulo': '1984',
                'propietario': biblio1,
                'puntuacion': 4,
                'comentario': 'Terroríficamente profética. Orwell describe un mundo que cada vez se parece más a nuestra realidad. El concepto de doblepensar es genial. Final devastador.',
                'fecha_lectura': date(2025, 1, 10),
            },
            {
                'libro_titulo': 'El Principito',
                'propietario': biblio1,
                'puntuacion': 5,
                'comentario': 'Un libro que se lee en una tarde pero se reflexiona toda la vida. "Lo esencial es invisible a los ojos." Perfecto para cualquier edad.',
                'fecha_lectura': date(2025, 8, 5),
            },
            {
                'libro_titulo': 'El nombre de la rosa',
                'propietario': biblio2,
                'puntuacion': 4,
                'comentario': 'Una novela compleja y fascinante. Eco mezcla el misterio con la erudición medieval de forma magistral. Los pasajes sobre la biblioteca son sublimes.',
                'fecha_lectura': date(2024, 11, 22),
            },
            {
                'libro_titulo': 'Tokio Blues (Norwegian Wood)',
                'propietario': biblio2,
                'puntuacion': 4,
                'comentario': 'Murakami en su faceta más realista y emotiva. Una novela nostálgica que transmite una melancolía hermosa. Los personajes son profundos y humanos.',
                'fecha_lectura': date(2025, 2, 14),
            },
            {
                'libro_titulo': 'Fahrenheit 451',
                'propietario': biblio2,
                'puntuacion': 5,
                'comentario': 'Imprescindible para cualquier amante de los libros. Bradbury imagina un futuro donde los libros son el enemigo. La escena final es pura poesía.',
                'fecha_lectura': date(2025, 5, 3),
            },
            {
                'libro_titulo': 'La sombra del viento',
                'propietario': biblio3,
                'puntuacion': 5,
                'comentario': 'Una carta de amor a los libros y a Barcelona. Zafón teje una trama adictiva en una ambientación perfecta. El Cementerio de los Libros Olvidados es un concepto maravilloso.',
                'fecha_lectura': date(2025, 4, 18),
            },
            {
                'libro_titulo': 'Orgullo y prejuicio',
                'propietario': biblio3,
                'puntuacion': 5,
                'comentario': 'Una novela encantadora con una protagonista adelantada a su tiempo. La ironía de Austen es deliciosa. Elizabeth Bennet es uno de los mejores personajes de la literatura.',
                'fecha_lectura': date(2024, 9, 7),
            },
        ]

        for resena_data in resenas_data:
            try:
                libro = Libro.objects.get(
                    titulo=resena_data['libro_titulo'],
                    propietario=resena_data['propietario']
                )
                resena, created = Resena.objects.get_or_create(
                    libro=libro,
                    defaults={
                        'puntuacion': resena_data['puntuacion'],
                        'comentario': resena_data['comentario'],
                        'fecha_lectura': resena_data['fecha_lectura'],
                    }
                )
                if created:
                    self.stdout.write(f'  Reseña creada: {libro.titulo} ({resena_data["puntuacion"]}★)')
            except Libro.DoesNotExist:
                pass

        # ====== PRÉSTAMOS ======
        prestamos_data = [
            {
                'libro_titulo': 'El Principito',
                'propietario': biblio1,
                'nombre_prestatario': 'Laura Torres',
                'fecha_prestamo': date(2025, 9, 1),
                'fecha_devolucion_esperada': date(2025, 10, 1),
                'fecha_devolucion_real': None,  # Aún prestado
                'notas': 'Lo necesita para un trabajo de clase',
            },
            {
                'libro_titulo': 'Rayuela',
                'propietario': biblio1,
                'nombre_prestatario': 'Pablo Hernández',
                'fecha_prestamo': date(2025, 6, 15),
                'fecha_devolucion_esperada': date(2025, 7, 15),
                'fecha_devolucion_real': date(2025, 7, 20),
                'notas': 'Devuelto en buen estado',
            },
            {
                'libro_titulo': 'El código Da Vinci',
                'propietario': biblio2,
                'nombre_prestatario': 'Sofía Ruiz',
                'fecha_prestamo': date(2025, 11, 10),
                'fecha_devolucion_esperada': date(2025, 12, 10),
                'fecha_devolucion_real': None,  # Aún prestado
                'notas': '',
            },
        ]

        for prestamo_data in prestamos_data:
            try:
                libro = Libro.objects.get(
                    titulo=prestamo_data['libro_titulo'],
                    propietario=prestamo_data['propietario']
                )
                prestamo, created = Prestamo.objects.get_or_create(
                    libro=libro,
                    nombre_prestatario=prestamo_data['nombre_prestatario'],
                    fecha_prestamo=prestamo_data['fecha_prestamo'],
                    defaults={
                        'fecha_devolucion_esperada': prestamo_data['fecha_devolucion_esperada'],
                        'fecha_devolucion_real': prestamo_data['fecha_devolucion_real'],
                        'notas': prestamo_data['notas'],
                    }
                )
                if created:
                    estado = 'prestado' if prestamo.esta_prestado else 'devuelto'
                    self.stdout.write(f'  Préstamo creado: {libro.titulo} -> {prestamo.nombre_prestatario} ({estado})')
            except Libro.DoesNotExist:
                pass

        # ====== LISTA DE DESEOS ======
        deseos_data = [
            {
                'usuario': biblio1,
                'titulo': 'Kafka en la orilla',
                'autor': 'Haruki Murakami',
                'isbn': '9788483835180',
                'notas': 'Quiero leer más de Murakami. Recomendado por Carlos.',
                'prioridad': 3,
            },
            {
                'usuario': biblio1,
                'titulo': 'Los pilares de la Tierra',
                'autor': 'Ken Follett',
                'isbn': '9788497594738',
                'notas': 'Novela histórica sobre la construcción de una catedral.',
                'prioridad': 2,
            },
            {
                'usuario': biblio1,
                'titulo': 'El infinito en un junco',
                'autor': 'Irene Vallejo',
                'isbn': '9788418173196',
                'notas': 'Historia de los libros y la lectura. Prioridad máxima.',
                'prioridad': 3,
            },
            {
                'usuario': biblio2,
                'titulo': 'Proyecto Hail Mary',
                'autor': 'Andy Weir',
                'isbn': '9788466668217',
                'notas': 'Del autor de El Marciano. Ciencia ficción hard.',
                'prioridad': 3,
            },
            {
                'usuario': biblio2,
                'titulo': 'Fundación',
                'autor': 'Isaac Asimov',
                'isbn': '9788497599245',
                'notas': 'Un clásico de la ciencia ficción que me falta por leer.',
                'prioridad': 2,
            },
            {
                'usuario': biblio3,
                'titulo': 'Persuasión',
                'autor': 'Jane Austen',
                'isbn': '9788491050193',
                'notas': 'La última novela de Austen. Dicen que es la más madura.',
                'prioridad': 3,
            },
            {
                'usuario': biblio3,
                'titulo': 'Circe',
                'autor': 'Madeline Miller',
                'isbn': '9788491813002',
                'notas': 'Mitología griega desde perspectiva femenina.',
                'prioridad': 2,
            },
        ]

        for deseo_data in deseos_data:
            deseo, created = ListaDeseos.objects.get_or_create(
                usuario=deseo_data['usuario'],
                titulo=deseo_data['titulo'],
                defaults=deseo_data
            )
            if created:
                self.stdout.write(f'  Deseo creado: {deseo.titulo} ({deseo.usuario.username})')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('¡Datos de ejemplo creados correctamente!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('Usuarios de prueba:')
        self.stdout.write(f'  Admin:        admin / admin1234')
        self.stdout.write(f'  Bibliotecario: maria_lectora / maria1234')
        self.stdout.write(f'  Bibliotecario: carlos_libros / carlos1234')
        self.stdout.write(f'  Bibliotecario: ana_biblioteca / ana12345')
        self.stdout.write(f'  Visitante:    pedro_visitante / pedro1234')
        self.stdout.write('')
        self.stdout.write(f'Total libros: {Libro.objects.count()}')
        self.stdout.write(f'Total reseñas: {Resena.objects.count()}')
        self.stdout.write(f'Total préstamos: {Prestamo.objects.count()}')
        self.stdout.write(f'Total deseos: {ListaDeseos.objects.count()}')
