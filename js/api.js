
const URL = 'wss://9ddqfj3crk.execute-api.sa-east-1.amazonaws.com/dev'

const Actions = {
    GET: 'GET',
    SET: 'SET',
    AREA: 'AREA'
}
Object.freeze(Actions)


class API extends WebSocket {
    constructor () {
        console.debug('Connecting')
        super(URL)
    }

    set (x, y, char) {
        char = char.charAt(0)
        console.debug(`SET: (${x}, ${y}) = '${char}'`)
        let data = { action: Actions.SET, x, y, char }
        data = JSON.stringify(data)
        return this.send(data)
    }

    get (x, y) {
        console.debug(`GET: (${x}, ${y})`)
        let data = { action: Actions.GET, x, y }
        data = JSON.stringify(data)
        return this.send(data)
    }

    area (x, y, width, heigth) {
        console.debug(`AREA: (${x}, ${y}, ${width}, ${heigth})`)

        const div = 10

        const divW = Math.floor(width / div)
        const modW = width % div

        for (let i = 0; i < div; i++) {
            let data = {
                action: Actions.AREA,
                x: x + i * divW,
                y,
                width: divW,
                heigth
            }
            data = JSON.stringify(data)
            this.send(data)
        }

        let data = {
            action: Actions.AREA,
            x: x + div * divW,
            y,
            width: modW,
            heigth
        }
        data = JSON.stringify(data)
        this.send(data)

        // let data = { action: Actions.AREA, x, y, width, heigth }
        // data = JSON.stringify(data)
        // return this.send(data)
    }
}
