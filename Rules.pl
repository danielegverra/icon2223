average(List, Average) :-
    sum_list(List, Sum),
    length(List, Length),
    Average is Sum / Length.

calculateDensity(PoiName, Density) :-
    findall(Dist, (distance(PoiName, _, Dist); distance(_, PoiName, Dist)), Dists),
    average(Dists, Density).

nextTo(FirstPoiName, SecondPoiName) :-
    distance(FirstPoiName, SecondPoiName, Distance),
    Distance < 300.

highlyRated(PoiName) :-
    rating(PoiName, Rating),
    Rating > 4.5.

popular(PoiName) :-
    ratingCount(PoiName, Count),
    Count > 1000.

highlyRecommended(PoiName) :-
    highlyRated(PoiName),
    popular(PoiName).

closeToCityCentre(PoiName) :-
    centreDistance(PoiName, Distance),
    Distance < 500.

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
    TourismRate > 1500000,
    TourismRateOutOfTen is 10.

calculateTourismRateOutOfTen(PoiName, TourismRateOutOfTen) :-
    tourismRate(PoiName, TourismRate),
    TourismRate =< 1500000,
    TourismRateOutOfTenFloat is (TourismRate - 200000) / 133333.3333,
    TourismRateOutOfTenInt is round(TourismRateOutOfTenFloat),
    TourismRateOutOfTen is min(max(TourismRateOutOfTenInt, 1), 10).

topTourismAttraction(PoiName) :-
    tourismRate(PoiName, Rate),
    Rate > 7.
