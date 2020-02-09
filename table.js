
class Table {
    constructor (cols, rows, element) {
        this.cols = cols
        this.rows = rows
        this.coord = { x: 0, y: 0 }
        this.table = element

        // Rows
        for (let i = 0; i < rows; i++) {
            const tr = document.createElement('tr')
            tr.id = i
            element.appendChild(tr)

            // Cols
            for (let j = 0; j < cols; j++) {
                const td = document.createElement('td')
                td.id = j
                tr.appendChild(td)
            }
        }

        this.select(0, 0)
    }

    current() {
        const { x, y } = this.coord
        return this.get(x, y)
    }

    get (x, y) {
        const tr = this.table.children[y]
        return tr.children[x]
    }

    set (x, y, c) {
        this.get(x, y).innerText = c.charAt(0)
        return this.get(x, y)
    }

    select (x, y) {
        const current = this.current()
        current.classList.remove('selected')

        this.coord = { x: Number.parseInt(x), y: Number.parseInt(y) }

        const cell = this.get(x, y)
        cell.classList.add('selected')
        return cell
    }
}
