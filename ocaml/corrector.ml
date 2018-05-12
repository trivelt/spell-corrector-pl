(* ocamlfind ocamlc -package core_extended -thread -linkpkg corrector.ml *)
open Core
open Core.Std
module StringSet = Set.Make(String)


let int_of_string_default str default =
  try
    int_of_string str
  with Failure "int_of_string" -> default

(* or return None/Some? *)
let line_to_pair line =
    let stripped_line = String.strip line in
    let splitted_line = String.split stripped_line ~on:' ' in
    let hd = List.hd_exn splitted_line in
    let frequency = int_of_string_default hd 0 in
    let word = List.nth splitted_line 1 in
    frequency, Option.value_exn word


let read_file filename = 
    let words =  Hashtbl.create ~hashable:String.hashable () in
    let chan = In_channel.create filename in 
    let num_of_line = ref 0 in
    try
        while true; do
            num_of_line := !num_of_line + 1;
            if (!num_of_line % 100000) = 0 then
                (print_int !num_of_line;
                print_endline "");
            
            let line = input_line chan in
            let freq, word = line_to_pair line in
(*            print_endline ("Set " ^ word ^ " = " ^ (string_of_int freq)); *)
            Hashtbl.set words word freq
        done; words
    with End_of_file ->
        In_channel.close chan;
        words

let rec splits word index l_splits = 
    let length = String.length word in
    let word_L = String.sub word 0 index in
    let word_R = String.sub word index (length - index) in
    let next_index = index + 1 in
    let l_splits = (word_L, word_R) :: l_splits in
    if next_index = length+1 then l_splits else splits word next_index l_splits


let rec print_list = function 
[] -> print_endline ""
| e::l -> 
    let a, b = e in 
    print_string a;
    print_string "-" ;
    print_string b;
    print_string ", ";
    print_list l

let rec print_list_sec = function 
[] -> print_endline ""
| e::l -> 
    print_string e;
    print_string ", ";
    print_list_sec l


let rec deletes l_splits l_deletes =
    match l_splits with
        | [] -> l_deletes
        | hd::tl -> 
            let word_L, word_R = hd in 
            let new_word_R = String.drop_prefix word_R 1 in
            let word_del = word_L ^ new_word_R in
            deletes tl (word_del::l_deletes)


let deletes l_splits = 
    List.map ~f:(fun x -> let x_L, x_R = x in x_L ^ (String.drop_prefix x_R 1)) l_splits


let get_char text n = 
    Char.to_string (String.get text n)

let transposes l_splits = 
    List.filter_map ~f:(fun x ->
        let x_L, x_R = x in 
        if String.length x_R > 1 then
            Some (x_L ^ 
            get_char x_R 1 ^
            get_char x_R 0 ^
            (String.drop_prefix x_R 2))
        else
            None
    ) l_splits


let rec change_splits l_splits l_output f =
    let letters = String.to_list "abcdefghijklmnopqrstuvwxyz" |> List.map ~f:(fun x -> Char.to_string x) in
    match l_splits with
            | [] -> l_output
            | (x_L, x_R)::tl -> change_splits tl (l_output @ List.fold letters ~init:[] ~f:(f x_L x_R)) f

let inserts l_splits = 
    change_splits l_splits [] (fun x_L x_R acc c -> (x_L ^ c ^ x_R) :: acc)

let replaces l_splits = 
    let replace_letter x_L x_R acc c = 
        if String.length x_R < 1 then acc
        else
            let word_R = String.drop_prefix x_R 1 in
            (x_L ^ c ^ word_R) :: acc
    in change_splits l_splits [] replace_letter


let append l1 l2 =
  let rec loop acc l1 l2 =
    match l1, l2 with
    | [], [] -> List.rev acc
    | [], h :: t -> loop (h :: acc) [] t
    | h :: t, l -> loop (h :: acc) t l
    in
    loop [] l1 l2


let flatten list =
  let rec aux accu = function
    | []          -> accu
    | []     :: t -> aux accu t
    | (x::y) :: t -> aux (x::accu) (y::t) in
  List.rev (aux [] list)
(* let flatten = List.fold_left ~init:[] ~f:(fun acc l -> acc @ l) *)

let edits1 word = 
    let splitted = splits word 0 [] in
    let deletes = deletes splitted in
    let transposes = transposes splitted in
    let replaces = replaces splitted in
    let inserts = inserts splitted in
(*    let candidates = deletes @ transposes @ replaces @ inserts in *)
    let candidates = append deletes (append transposes (append replaces inserts)) in
    let set = List.fold_left candidates ~f:(fun set elem -> StringSet.add set elem) ~init:StringSet.empty in
    StringSet.to_list set


let edits2 word = 
    let l_edits1 = edits1 word in
    let l_edits2 = List.map ~f:(fun word -> edits1 word) l_edits1 in
    flatten l_edits2

let get_candidates word = 
    edits1 word

let get_known_candidates known_words candidates = 
    List.filter candidates ~f:(fun x -> 
        match Hashtbl.find known_words x with 
            | None -> false
            | Some _ -> true)

let sort_by_P known_words candidates = 
    List.sort ~cmp:(fun a b -> 
        let a_P = Hashtbl.find known_words a in
        let b_P = Hashtbl.find known_words b in
        match a_P, b_P with
            | None, None -> 0
            | None, Some b -> 1
            | Some a, None -> -1
            | Some a, Some b -> b-a
    ) candidates

let correction word =
    let known_words = read_file "../n-grams/1grams_fixed" in
    let candidates = get_candidates word in
    let candidates = get_known_candidates known_words candidates in
(*    let _ = print_list_sec candidates in *)
    let sorted_candidates = sort_by_P known_words candidates in
    if (List.length sorted_candidates) > 0 then
        List.hd_exn sorted_candidates
    else
        "Not found"

(*    let is_known = Hashtbl.find known_words word in
    word
*)


let () = 
    let word = correction "pogramowanie" in
    print_endline "OCaml Corrector";
    print_endline word;

    let s = splits "hello" 0 [] in
    print_list s

