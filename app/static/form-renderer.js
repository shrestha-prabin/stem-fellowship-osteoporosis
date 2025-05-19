
const formContent = document.getElementById("form-content");


fetch('static/data.json').then(res => res.json()).then(data => {
  const formInputs = []

  data.forEach((item) => {
    switch (item.type) {
      case "boolean":
        formInputs.push(`
          <li>
            <div>
              <label class='font-medium'>${item['question']}</label>
              <div class='flex flex-row space-x-4'>
                <div>
                  <input type='radio' id='${item['name']}-yes' name='${item['name']}' value='Yes' />
                  <label for='${item['name']}-yes'>Yes<label>
                </div>
                <div>
                  <input type='radio' id='${item['name']}-no' name='${item['name']}' value='No' />
                  <label for='${item['name']}-no'>No<label>
                </div>
              </div>
            </div>
          </li>
        `)
        break;

      case "select":
        const options = []
        for (const option of item['options']) {
          options.push(`
            <div>
              <input type='radio' id='${item['name']}-${option}' name='${item['name']}' value='${option}' />
              <label for='${item['name']}-${option}'>${option}<label>
            </div> 
          `)
        }

        formInputs.push(`
          <li>
            <label class='font-medium'>${item['question']}</label>
            <div>
              ${options.join('')} 
            </div>
          </li>
        `)
        break;

      case "multiselect":
        const multiselectOptions = []
        for (const option of item['options']) {
          multiselectOptions.push(`
            <div>
              <input type='checkbox' id='${item['name']}-${option}' name='${item['name']}' value='${option}' />
              <label for='${item['name']}-${option}'>${option}<label>
            </div> 
          `)
        }

        formInputs.push(`
          <li>
            <label class='font-medium'>${item['question']}</label>
            <div>
              ${multiselectOptions.join('')} 
            </div>
          </li>
        `)
        break;

      default:
        formInputs.push(`
          <li>
            <div class='grid'>
              <label class='font-medium'>${item['question']}</label>
              <input class='border border-gray-400 bg-gray-50 rounded outline-none px-2 h-8 focus:ring-2 focus:ring-indigo-300' id='${item['name']}' name='${item['name']}' type='${item['type']}' />
            </div>
          </li>
        `)
        break;
    }
  })

  formContent.innerHTML = `
    <ol class='list-decimal grid grid-cols-1 gap-6'>
      ${formInputs.join('')}
    </ol>
  `
})

