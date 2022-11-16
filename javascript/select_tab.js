function select_tab(index){
  let tab_base = gradioApp().querySelector("#tab_merge_board");
  let buttons = gradioApp().querySelector("#tab_merge_board").querySelectorAll("Button");

  let btn = buttons[index];

  btn.click();
}

function select_tab_merge(){
  select_tab(0);
  return args_to_array(arguments);
}

function select_tab_recipe(){
  select_tab(1);
  return args_to_array(arguments);
}
