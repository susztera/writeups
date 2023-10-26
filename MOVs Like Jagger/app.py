@app.route('/api/coordinates', methods=['GET'])
def coordinates():
    points = {
        'departed_x': hex(Q.x()), 'departed_y': hex(Q.y()),
        'present_x': hex(P.x()), 'present_y': hex(P.y())
    }
    return points


@app.route('/api/get_flag', methods=['POST'])
def get_flag():
    try:
        travel_result = checkDestinationPoint(request.json, P, nQ, E)
        location = generateLocation(travel_result)

        if travel_result:
            return {"location": location, "flag": FLAG}
        else:
            return {"location": location}
    except ValueError as error:
        return {"error": error}


if __name__ == '__main__':
    Q, nQ, P, nP = calculatePointsInSpace()
    app.run(host='0.0.0.0', port=1337, debug=False, use_reloader=False)
