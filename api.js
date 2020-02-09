
const URL = 'wss://9ddqfj3crk.execute-api.sa-east-1.amazonaws.com/dev'

const Actions = {
    GET: 'GET',
    SET: 'SET',
    AREA: 'AREA'
}
Object.freeze(Actions)


class API extends WebSocket {
    constructor () {
        super(URL)
    }

    set (x, y, char) {
        let data = { action: Actions.SET, x, y, char }
        data = JSON.stringify(data)
        return this.send(data)
    }

    get (x, y) {
        let data = { action: Actions.GET, x, y }
        data = JSON.stringify(data)
        return this.send(data)
    }

    area (x, y, width, heigth) {
        let data = { action: Actions.AREA, x, y, width, heigth }
        data = JSON.stringify(data)
        return this.send(data)
    }
}
