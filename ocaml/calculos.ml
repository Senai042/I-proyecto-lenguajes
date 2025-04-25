open Yojson.Basic
open Yojson.Basic.Util
module StringMap = Map.Make(String)

let redondear_decimales n decimales =
  let factor = 10. ** float_of_int decimales in
  floor (n *. factor +. 0.5) /. factor

let limitar_100 n =
  if n > 100.0 then 100.0 else n

<<<<<<< HEAD
=======
(* Acumulador para listas con suma y conteo *)
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
let actualizar_promedios mapa clave valor =
  let suma, cuenta =
    match StringMap.find_opt clave mapa with
    | Some (s, c) -> (s +. valor, c + 1)
    | None -> (valor, 1)
  in
  StringMap.add clave (suma, cuenta) mapa

<<<<<<< HEAD
(* Función para tomar los primeros n elementos de una lista *)
let rec take n lst =
  match lst with
  | [] -> []
  | x :: xs -> if n <= 0 then [] else x :: take (n - 1) xs

(* Detectar la tendencia del estudiante entre parciales *)
let clasificar_tendencia p1 p2 p3 =
  if p1 < p2 && p2 < p3 then "mejora"
  else if p1 > p2 && p2 > p3 then "caída"
  else "estable"

let () =
  let json = from_file "./curso_estudiantes.json" in
=======
let () =
  let json = from_file "../curso_estudiantes.json" in
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
  let evaluaciones = json |> member "evaluaciones" |> to_list in
  let estudiantes = json |> member "estudiantes" |> to_list in

  let peso_map =
    List.fold_left (fun acc ev ->
      let id = ev |> member "id" |> to_string in
      let peso = ev |> member "peso" |> to_number in
      StringMap.add id peso acc
    ) StringMap.empty evaluaciones
  in

  let eval_subtemas_map =
    List.fold_left (fun acc ev ->
      let id = ev |> member "id" |> to_string in
      let subtemas = ev |> member "subtemas" |> to_list |> List.map to_string in
      StringMap.add id subtemas acc
    ) StringMap.empty evaluaciones
  in

  let resultados, acumulador_subtemas, notas_finales =
    List.fold_left (fun (acum, map_subtemas, todas_las_notas) est ->
      let id = est |> member "id" |> to_string in
      let nombre = est |> member "nombre" |> to_string in
      let evs = est |> member "evaluaciones" in

      let nota_final, notas_por_eval, conocimientos =
        StringMap.fold (fun eid peso (acc_final, evals_map, subtema_map) ->
          let ev_json = evs |> member eid in
          let nota_eval = ev_json |> member "nota" |> to_number in
          let nueva_nota = acc_final +. (nota_eval *. peso) in
          let evals_map = StringMap.add eid nota_eval evals_map in
          let subtemas = StringMap.find eid eval_subtemas_map in
          let subtema_notas = ev_json |> member "subtemas" in

          let subtema_map =
            List.fold_left (fun m st ->
              let nota_st = subtema_notas |> member st |> to_number in
              actualizar_promedios m st nota_st
            ) subtema_map subtemas
          in

          (nueva_nota, evals_map, subtema_map)
        ) peso_map (0.0, StringMap.empty, StringMap.empty)
      in

      let conocimiento_json =
        StringMap.bindings conocimientos
        |> List.map (fun (st_id, (suma, count)) ->
          let prom = redondear_decimales (suma /. float_of_int count) 1 in
          (st_id, `Float (limitar_100 prom))
        )
        |> List.sort (fun (a, _) (b, _) -> compare a b)
        |> fun lst -> `Assoc lst
      in

      let notas_eval_json =
        StringMap.bindings notas_por_eval
        |> List.map (fun (eid, n) ->
          let nota_redondeada = redondear_decimales n 1 in
          (eid, `Float (limitar_100 nota_redondeada))
        )
        |> List.sort (fun (a, _) (b, _) -> compare a b)
        |> fun lst -> `Assoc lst
      in

<<<<<<< HEAD
      let tendencia =
        try
          let p1 = StringMap.find "P1" notas_por_eval
          and p2 = StringMap.find "P2" notas_por_eval
          and p3 = StringMap.find "P3" notas_por_eval in
          `String (clasificar_tendencia p1 p2 p3)
        with _ -> `String "desconocida"
      in

=======
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
      let estudiante_json =
        `Assoc [
          ("id", `String id);
          ("nombre", `String nombre);
          ("nota_final", `Float (limitar_100 (redondear_decimales nota_final 1)));
          ("notas_evaluaciones", notas_eval_json);
<<<<<<< HEAD
          ("porcentaje_conocimiento", conocimiento_json);
          ("tendencia", tendencia)
=======
          ("porcentaje_conocimiento", conocimiento_json)
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
        ]
      in

      let map_subtemas =
        StringMap.fold (fun st (s, _) acc ->
          actualizar_promedios acc st s
        ) conocimientos map_subtemas
      in

      (estudiante_json :: acum, map_subtemas, nota_final :: todas_las_notas)
<<<<<<< HEAD
    ) ([], StringMap.empty, []) estudiantes
=======
    ) ([], StringMap.empty, [])
    estudiantes
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
  in

  let promedio lst = List.fold_left ( +. ) 0.0 lst /. float_of_int (List.length lst) in
  let moda lst =
    lst
    |> List.fold_left (fun m x ->
         let count = match StringMap.find_opt (string_of_float x) m with
           | Some c -> c + 1
           | None -> 1
         in StringMap.add (string_of_float x) count m
       ) StringMap.empty
    |> StringMap.bindings
    |> List.sort (fun (_, a) (_, b) -> compare b a)
    |> List.hd
    |> fun (n, _) -> float_of_string n
  in

  let nota_prom = redondear_decimales (promedio notas_finales) 1 in
  let nota_min = redondear_decimales (List.fold_left min max_float notas_finales) 1 in
  let nota_max = redondear_decimales (List.fold_left max min_float notas_finales) 1 in
  let nota_moda = redondear_decimales (moda notas_finales) 1 in

  let promedio_por_subtema =
    StringMap.bindings acumulador_subtemas
    |> List.map (fun (st, (suma, count)) ->
      let prom = redondear_decimales (suma /. float_of_int count) 1 in
      (st, `Float (limitar_100 prom))
    )
    |> List.sort (fun (a, _) (b, _) -> compare a b)
    |> fun lst -> `Assoc lst
  in

<<<<<<< HEAD
  let subtemas_criticos =
    StringMap.bindings acumulador_subtemas
    |> List.map (fun (st, (suma, count)) ->
      let prom = redondear_decimales (suma /. float_of_int count) 1 in
      (st, prom)
    )
    |> List.sort (fun (_, a) (_, b) -> compare a b)
    |> take 3
    |> List.map (fun (st, prom) -> (st, `Float prom))
    |> fun lst -> `Assoc lst
  in

=======
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
  let out_json =
    `Assoc [
      ("resultados", `List (List.rev resultados));
      ("estadisticas", `Assoc [
         ("nota_promedio", `Float nota_prom);
         ("nota_min", `Float nota_min);
         ("nota_max", `Float nota_max);
         ("nota_moda", `Float nota_moda);
<<<<<<< HEAD
         ("promedio_por_subtema", promedio_por_subtema);
         ("subtemas_criticos", subtemas_criticos)
=======
         ("promedio_por_subtema", promedio_por_subtema)
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
       ])
    ]
  in

<<<<<<< HEAD
  to_file "../resultados.json" out_json
=======
  Yojson.Basic.to_file "../resultados.json" out_json
>>>>>>> f59d68e636ce625c1aebf17898baa5500a22fc06
