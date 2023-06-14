average(List, Average) :-
    sum_list(List, Sum),
    length(List, Length),
    Average is Sum / Length.

calculateDensity(PoiName, Density) :-
    findall(Dist, (distance(PoiName, _, Dist); distance(_, PoiName, Dist)), Dists),
    average(Dists, Density).

nextTo(FirstPoiName, SecondPoiName) :-
    (distance(FirstPoiName, SecondPoiName, Distance); distance(SecondPoiName, FirstPoiName, Distance)),
    Distance < 501.

highlyRated(PoiName) :-
    rating(PoiName, Rating),
    Rating > 4.5.

popular(PoiName) :-
    ratingCount(PoiName, Count),
    Count > 15000.

highlyRecommended(PoiName) :-
    highlyRated(PoiName),
    popular(PoiName).

closeToCityCentre(PoiName) :-
    centreDistance(PoiName, Distance),
    Distance < 501.

cheap(PoiName) :-
    price(PoiName, Price),
    Price < 10.

ancient(PoiName) :-
    age(PoiName, Age),
    Age > 800.

impressive(PoiName) :-
    surface(PoiName, Surface),
    height(PoiName, Height),
    (Surface > 7000 ; Height > 17).

calculateTourismRateOutOfTen(PoiName, TourismRateOutOfTen) :-
    tourismRate(PoiName, TourismRate),
    TourismRateOutOfTenFloat is (TourismRate - 200000) / 133333.3333,
    TourismRateOutOfTenInt is round(TourismRateOutOfTenFloat),
    TourismRateOutOfTen is min(max(TourismRateOutOfTenInt, 1), 10).

topTourismAttraction(PoiName) :-
    tourismRateOutOfTen(PoiName, Rate),
    Rate > 7.

calculateTimeToVisit(PoiName, TimeToVisit) :-
    tourismRate(PoiName, TourismRate),
    surface(PoiName, Surface),
    height(PoiName, Height),
    normalizeTourismRate(TourismRate, NormTourismRate),
    normalizeSurface(Surface, NormSurface),
    normalizeHeight(Height, NormHeight),
    TimeToVisitNormalized is (NormTourismRate + NormSurface + NormHeight) / 3,
    TimeToVisitFloat is round(TimeToVisitNormalized * (40 - 5) + 5),
    TimeToVisit is min(max(TimeToVisitFloat, 5), 60).

normalizeTourismRate(TourismRate, NormTourismRate) :-
    NormTourismRate is (TourismRate - 200000) / 1333333.3333.

normalizeSurface(Surface, NormSurface) :-
    NormSurface is (Surface - 400) / 7600.

normalizeHeight(Height, NormHeight) :-
    NormHeight is Height / 20.

calculateTourismPriority(PoiName, TourismPriority) :-
    rating(PoiName, Rating),
    (popular(PoiName) ->
        PopularWeight = 0.6;
        PopularWeight = 0),
    (closeToCityCentre(PoiName) ->
        CloseToCityCentreWeight = 0.3;
        CloseToCityCentreWeight = 0),
    calculateTourismRateOutOfTen(PoiName, TourismRateOutOfTen),
    (ancient(PoiName) ->
        AncientWeight = 0.2;
        AncientWeight = 0),
    (impressive(PoiName) ->
        ImpressiveWeight = 0.3;
        ImpressiveWeight = 0),
    calculateDensity(PoiName, Density),
    NormalizedDensity is (Density - 1138) / (2846 - 1138),
    DensityWeight = 0.6 - (0.6 * NormalizedDensity),
    TourismPriority is Rating / 2 + PopularWeight + CloseToCityCentreWeight + TourismRateOutOfTen * 0.05 + AncientWeight + ImpressiveWeight + DensityWeight.

findDistance(PoiName1, PoiName2, Distance) :-
    distance(PoiName1, PoiName2, Distance).

findDistance(PoiName1, PoiName2, Distance) :-
    distance(PoiName2, PoiName1, Distance).

connectivityCheck(PoiName) :-
    findall(Dist, (distance(PoiName, _, Dist); distance(_, PoiName, Dist)), Dists),
    min_list(Dists, MinDistance),
    MinDistance < 501.

findNeighbors(PoiName, Neighbors) :-
    findall(Neigh, nextTo(PoiName, Neigh), Neighbors).

findMinDistance(Distance) :-
    findall(Dist, distance(_, _, Dist), Distances),
    min_list(Distances, Distance).

findMaxPrice(MaxPrice) :-
    findall(Price, price(_, Price), Prices),
    max_list(Prices, MaxPrice).

findMaxTimeToVisit(MaxTimeToVisit) :-
    findall(TimeToVisit, calculateTimeToVisit(_, TimeToVisit), TimesToVisit),
    max_list(TimesToVisit, MaxTimeToVisit).
