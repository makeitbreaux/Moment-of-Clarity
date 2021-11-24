$('.delete-drink').click(deleteDrink)

async function deleteDrink() {
  const id = $(this).data('id')
  await axios.delete(`/api/drinks/${id}`)
  $(this).parent().remove()
}

$('.add-drink').on('click', addDrink)
async function addDrink(e) {  
  await axios.post(`/add_drink`, JSON.parse(e.target.value));
}
