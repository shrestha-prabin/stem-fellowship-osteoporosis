
const formContent = document.getElementById("form-content");


fetch('static/data.json').then(res => res.json()).then(data => {
  const formInputs = []

  data.forEach((item) => {
    switch (item.type) {
      case "boolean":
        const defaultVal = item.default === false ? "No" : item.default === true ? "Yes" : null;

        formInputs.push(`
          <li id='q-${item['name']}'>
            <div>
              <label class='font-medium'>${item['question']}</label>
              <div class='flex flex-row space-x-4'>
                <div>
                  <label for='${item['name']}-yes'>
                    <input type='radio' id='${item['name']}-yes' name='${item['name']}' value='Yes' ${defaultVal === "Yes" ? "checked" : ""} />
                    Yes
                  </label>
                </div>
                <div>
                  <label for='${item['name']}-no'>
                    <input type='radio' id='${item['name']}-no' name='${item['name']}' value='No' ${defaultVal === "No" ? "checked" : ""} />
                    No
                  </label>
                </div>
              </div>
            </div>
          </li>
        `);
      break;

      case "select":
        const options = []
        for (const option of item['options']) {
          options.push(`
            <div>
              <label for='${item['name']}-${option}'>
                <input type='radio' id='${item['name']}-${option}' name='${item['name']}' value='${option}' />
                ${option}
              <label>
            </div> 
          `)
        }

        formInputs.push(`
          <li id='q-${item['name']}'>
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
              <label for='${item['name']}-${option}'>
                <input type='checkbox' id='${item['name']}-${option}' name='${item['name']}' value='${option}' />
                ${option}
              <label>
            </div> 
          `)
        }

        formInputs.push(`
          <li id='q-${item['name']}'>
            <label class='font-medium'>${item['question']}</label>
            <div>
              ${multiselectOptions.join('')} 
            </div>
          </li>
        `)
        break;

      default:
        formInputs.push(`
          <li id='q-${item['name']}'>
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

  const femaleOnlyInputs = data.filter(v => v.femaleOnly).map(v => v.name)
  console.log("🚀 ~ fetch ~ femaleOnlyInputs:", femaleOnlyInputs)

  document.getElementById('gender-Male').addEventListener('change', (e) => {
    femaleOnlyInputs.forEach(input => {
      document.getElementById(`q-${input}`).style.display = 'none'
    });
  })

  document.getElementById('gender-Female').addEventListener('change', (e) => {
    femaleOnlyInputs.forEach(input => {
      document.getElementById(`q-${input}`).style.display = 'list-item'
    });
  })
})

