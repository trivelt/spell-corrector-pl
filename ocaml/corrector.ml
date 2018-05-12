(* ocamlfind ocamlc -package core_extended -thread -linkpkg corrector.ml *)
open Core
open Core.Std
module StringSet = Set.Make(String)

let line_to_pair line = 
    let stripped_line = String.strip line in 
    let splitted_line = String.split stripped_line ~on:' ' in
    let hd = List.hd splitted_line in
    let word = List.nth splitted_line 1 in
    match hd, word with
        | None, _ | _, None -> 0, ""
        | Some x, Some y -> int_of_string x, y

let read_file filename =
    let words =  Hashtbl.create ~hashable:String.hashable () in
    let chan = In_channel.create filename in
    let num_of_line = ref 0 in
    let () = print_string "Loading known words" in
    try
        while true; do
            num_of_line := !num_of_line + 1;
            if (!num_of_line % 100000) = 0 then
                (print_string "."; flush stdout);

            let line = input_line chan in
            let freq, word = line_to_pair line in
            Hashtbl.set words word freq
        done; words
    with End_of_file ->
        In_channel.close chan;
        let () = print_endline " [OK]" in
        words

let load_known_words () =
    read_file "../n-grams/1grams_fixed"

let rec splits word index l_splits =
    let length = String.length word in
    let word_L = String.sub word 0 index in
    let word_R = String.sub word index (length - index) in
    let next_index = index + 1 in
    let l_splits = (word_L, word_R) :: l_splits in
    if next_index = length+1 then l_splits else splits word next_index l_splits

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

let flatten list =
  let rec aux accu = function
    | []          -> accu
    | []     :: t -> aux accu t
    | (x::y) :: t -> aux (x::accu) (y::t) in
  List.rev (aux [] list)

let edits1 word =
    let splitted = splits word 0 [] in
    let deletes = deletes splitted in
    let transposes = transposes splitted in
    let replaces = replaces splitted in
    let inserts = inserts splitted in
    let candidates = deletes @ transposes @ replaces @ inserts in
    let set = List.fold_left candidates ~f:(fun set elem -> StringSet.add set elem) ~init:StringSet.empty in
    StringSet.to_list set

let edits2 word =
    let l_edits1 = edits1 word in
    let l_edits2 = List.map ~f:(fun word -> edits1 word) l_edits1 in
    flatten l_edits2

let known_word known_words word =
    match Hashtbl.find known_words word with 
        | None -> false
        | Some _ -> true

let get_known_candidates known_words candidates =
    List.filter candidates ~f:(known_word known_words)

let get_candidates word known_words =
    match known_word known_words word with
        | true -> [word]
        | false -> 
            let known_edits1 = edits1 word |> get_known_candidates known_words in
            if List.length known_edits1 = 0 then
                edits2 word |> get_known_candidates known_words
            else
                known_edits1

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

let correction word known_words =
    let candidates = get_candidates word known_words in
    let sorted_candidates = sort_by_P known_words candidates in
    if (List.length sorted_candidates) > 0 then
        List.hd_exn sorted_candidates
    else
        word

let is_interactive_mode =
    match Array.find Sys.argv ~f:(fun arg -> arg = "-i") with
        | None -> false
        | Some _ -> true

let read_args () = 
    for i = 0 to Array.length Sys.argv - 1 do
      printf "[%i] %s\n" i Sys.argv.(i)
    done

let get_input_phrase () =
    match Array.length Sys.argv with
        | 1 -> ""
        | _ -> Array.get Sys.argv 1

let print_help () =
    let () = print_endline 
        ("Usage: ./corector -i to run in interactive mode, " ^ 
        "or ./corrector \"phrase to correct\" to use non-interactive mode")
    in
    exit 0

let correct_phrase phrase known_words =
    let rec correct_words l_words =
        match l_words with
            | [] -> ()
            | word :: tl -> 
                let () = correction word known_words ^ " "|> print_string in
                correct_words tl
    in
    let () = String.split phrase ~on:' ' |> correct_words in
    print_endline ""

let rec process_input_interactively known_words =
    let () = print_string "> " in
    let text = read_line () in
    let () = correct_phrase text known_words in
    process_input_interactively known_words

let correct_input_phrase () =
    let phrase = get_input_phrase () in
    match phrase with
        | "" | "-h" -> print_help ()
        | phrase -> correct_phrase phrase (load_known_words ())

let () =
    match is_interactive_mode with
        | true ->  process_input_interactively (load_known_words ())
        | false -> correct_input_phrase ()

