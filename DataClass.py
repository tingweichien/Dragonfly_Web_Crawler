class simplifyTableInfo:
    def __init__(self, IdNumber, Dates, Times, City, Dictrict, Place, Altitude):
        self.IdNumber = IdNumber
        self.Dates = Dates
        self.Times = Times
        self.City = City
        self.Dictrict = Dictrict
        self.Place = Place
        self.Altitude = Altitude
    
    def __str__(self):
        return ('\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [Dictrict]: ' + self.Dictrict +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]:'  + self.Place )



class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber, Dates, Times, City, Dictrict, Place, Altitude, Lateral, Longitude, Species, Description):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, Dictrict, Place, Altitude)
        self.Lateral = Lateral
        self.Longitude = Longitude
        self.Species = Species
        self.Description = Description
    def __str__(self):
        return (super(simplifyTableInfo, self).__str__ +
                '\t[Lateral]: ' + self.Lateral +
                '\t[Longitude]: ' + self.Longitude +
                '\t[Species]: ' + self.Species +
                '\t[Description]: ' + self.Description)