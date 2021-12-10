$('.delete-drink').click(deleteDrink)

async function deleteDrink() {
  const drinkName = $(this).data('drinkName')
  await axios.delete(`/drink/${drinkName}`)
  $(this).parent().remove()
}

// $('.add-drink').click(addDrink)

// async function addDrink() {
//   const drinkName = $(this).data('drinkName')
//   await axios.add(`/drink/${drinkName}`)
//   $(this).parent().add()
// }
