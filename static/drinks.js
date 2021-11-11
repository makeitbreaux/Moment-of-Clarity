$('.delete-drink').click(deleteDrink)

async function deleteDrink() {
  const id = $(this).data('id')
  await axios.delete(`/api/drinks/${id}`)
  $(this).parent().remove()
}

