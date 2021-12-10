// TRYING TO GET DELETE BUTTON ON /SHOW_DRINKS TO WORK
$('.delete-drink').click(deleteDrink)

async function deleteDrink() {
  const drinkName = $(this).data('drinkName')
  await axios.delete(`/drink/${drinkName}`)
  $(this).parent().remove()
}

// TRYING TO GET ADD BUTTON ON /SHOW_DRINKS TO WORK
// $('.add-drink').click(addDrink)

// async function addDrink() {
//   const drinkName = $(this).data('drinkName')
//   await axios.add(`/drink/${drinkName}`)
//   $(this).parent().add()
// }
