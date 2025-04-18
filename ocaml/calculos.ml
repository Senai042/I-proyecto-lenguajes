(* ocaml/calculos.ml *)
open Yojson.Basic
open Yojson.Basic.Util

let () =
  (* 1 Cargo el JSON de entrada *)
  let json = from_file "../curso_estudiantes.json" in

  (* 2 Construyo la lista (evaluacion_id * peso) *)
  let peso_map =
    json
    |> member "evaluaciones"
    |> to_list
    |> List.map (fun ev ->
         let id   = ev |> member "id"   |> to_string in
         let peso = ev |> member "peso" |> to_number in
         (id, peso)
       )
  in

  (* 3 Para cada estudiante calculo la nota final *)
  let results =
    json
    |> member "estudiantes"
    |> to_list
    |> List.map (fun st ->
         let id     = st |> member "id"     |> to_string in
         let nombre = st |> member "nombre" |> to_string in
         let evs    = st |> member "evaluaciones" in
         let nota_final =
           List.fold_left (fun acc (eid, peso) ->
             let nota = evs
                        |> member eid
                        |> member "nota"
                        |> to_number
             in
             acc +. peso *. nota
           ) 0.0 peso_map
         in
         (id, nombre, nota_final)
       )
  in

  (* 4 Calculo la nota mínima y máxima *)
  let notas = List.map (fun (_,_,nf) -> nf) results in
  let min_n = List.fold_left min (List.hd notas) notas in
  let max_n = List.fold_left max (List.hd notas) notas in

  (* 5 Empaqueto todo en un nuevo JSON *)
  let out_json =
    `Assoc [
      ("results",
        `List (List.map (fun (id,nombre,nf) ->
           `Assoc [
             ("id",         `String id);
             ("nombre",     `String nombre);
             ("nota_final", `Float  nf)
           ]
         ) results)
      );
      ("min", `Float min_n);
      ("max", `Float max_n)
    ]
  in

  (* 6 Guardo el JSON en un archivo para Python *)
  Yojson.Basic.to_file "../resultados.json" out_json
