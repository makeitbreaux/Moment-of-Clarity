// TRYING TO GET DELETE BUTTON ON /SHOW_DRINKS TO WORK
// $('#delete-drink').click(deleteDrink)

// async function deleteDrink(e) {
//   e.preventDefault();
//     const drink_name = $("#drink_name").text();
//     const tags = $("#drink_tags").text();
//     const category = $("#drink_category").text();
//     const glass = $("#drink_glass").text();
//     const instructions = $("#drink_instructions").text();
//     const ingredients = $("#drink_ingredients").text();
//     const measures = $("#drink_measures").text();
//     const image_thumb = $("#drink_image_thumb").attr('src');
    
//     await axios.delete(`/recipes`, {
//       drink_name,
//       tags,
//       category,
//       glass,
//       instructions,
//       ingredients,
//       measures,
//       image_thumb
//     });

//     $("#container").hide();
//   }


$('#add-drink').click(addDrink)

async function addDrink(e) {
  e.preventDefault();
  const drink_name = $("#drink_name").text();
  const tags = $("#drink_tags").text();
  const category = $("#drink_category").text();
  const glass = $("#drink_glass").text();
  const instructions = $("#drink_instructions").text();
  const ingredients = $("#drink_ingredients").text();
  const measures = $("#drink_measures").text();
  const image_thumb = $("#drink_image_thumb").attr('src');
  
  await axios.post(`/add_drink`, {
    drink_name,
    tags,
    category,
    glass,
    instructions,
    ingredients,
    measures,
    image_thumb
  });
 //DISABLE BUTTON AFTER DRINK ADDED
  $('#add-drink').attr("disabled", true);

}


