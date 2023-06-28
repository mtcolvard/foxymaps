import React from 'react'
import axios from 'axios'
import ReactMapGl, {MapGl, BaseControl, NavigationControl, ScaleControl, GeolocateControl, LinearInterpolator, FlyToInterpolator, HTMLOverlay, Layer, Source, WebMercatorViewport} from 'react-map-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import SearchBar from './SearchBar'
import SearchBarDirections from './SearchBarDirections'
import DropDownDisplay from './DropDownDisplay'
import BottomDestinationDisplay from './BottomDestinationDisplay'
import ShouldTheRouteBeDisplayed  from './ShouldTheRouteBeDisplayed'
import ShouldTheParksDisplayUpdate from './ShouldTheParksDisplayUpdate'
import CommuteVsExplore from './CommuteVsExplore'
import ExploreOptions from './ExploreOptions'
import Pins from './Pins'

const lngLat = [-0.097865,51.514014]
const deltaTime = 0
const routeGeometryStateDefault = {
  'type': 'Feature',
  'properties': {'name': null},
  'geometry': {
    'type': 'Point',
    'coordinates': [-0.097865,51.514014]}
}



const searchReponseStateDefault = {
  type: null,
  query: [null],
  features: [
    {place_type: [null]}
  ],
  attribution: null
}

class Map extends React.Component {
  constructor() {
    super()

    this.state = {
      ramblingTolerance: '1000',
      angleFilter: '45',
      originFormData: '',
      destinationFormData: '',
      originData: '',
      destinationData: '',
      originLonLat: null,
      destinationLonLat: null,
      routeGeometry: routeGeometryStateDefault,
      routeLargestPark: {},
      viewport: {
        longitude: -0.097865,
        latitude: 51.514014,
        zoom: 11,
        altitude: 0.75,
      },
      geolocateClick: false,
      searchResponseData: {
        type: null,
        query: [null],
        features: [{place_type: [null]}],
        attribution: null},
      isSearchTriggered: false,
      isoriginFormDataSearchTriggered: false,
      isdestinationFormDataSearchTriggered: false,
      isRouteSelected: false,
      displayDirectionsSearchBar: false,
      displayOriginSearchBar: false,
      displayOriginSearchOptions: false,
      displayDestinationSearchBar: true,
      displayBottomDestinationData: false,
      displayCommuteVsExplore: true,
      loadingSpinner: false,
      isMapboxSearching: false,
      routePins: [],
      allParkPins: [],
      publicButton: true,
      publicPrivateButton: false,
      privateButton: false,
      parkAccessFilter: 'publicParks',
      toggleExplore: false,
      toggleRecalculate: false,
      route_waypoints_lon_lat_formatted: '',
      compass_and_radius_routing_option_formatted: '',
      sizeFormData: 0.28,
    }
    this.handleViewportChange =this.handleViewportChange.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleClear = this.handleClear.bind(this)
    this.handleDirectionsButtonClick = this.handleDirectionsButtonClick.bind(this)
    this.handleDirectionsSearchBarArrowLeft = this.handleDirectionsSearchBarArrowLeft.bind(this)
    this.handleOriginSearchBarArrowLeft = this.handleOriginSearchBarArrowLeft.bind(this)
    this.displayOriginSearchMenu = this.displayOriginSearchMenu.bind(this)
    this.displayDestinationSearchMenu = this.displayDestinationSearchMenu.bind(this)
    this.handleReverseOriginAndDestination = this.handleReverseOriginAndDestination.bind(this)
    this.displaySelectedDestinationData = this.displaySelectedDestinationData.bind(this)
    this.displaySelectedOriginData = this.displaySelectedOriginData.bind(this)
    this.sendDestinationToBackend = this.sendDestinationToBackend.bind(this)
    this.handleFindMyLocation = this.handleFindMyLocation.bind(this)
    this.chooseLocationOnMap = this.chooseLocationOnMap.bind(this)
    this.handleMapClick = this.handleMapClick.bind(this)
    this.handleExploreOptionsButtonsClick = this.handleExploreOptionsButtonsClick.bind(this)
    this.handleToggleExploreClick = this.handleToggleExploreClick.bind(this)
    this.handleRecalculate = this.handleRecalculate.bind(this)
    this.queryBackendForRouteGeometry = this.queryBackendForRouteGeometry.bind(this)
    this.updateParksFromExploreOptions = this.updateParksFromExploreOptions.bind(this)
    // this.handleMouseUp = this.handleMouseUp.bind(this)
    // this.handleMouseUpSubmit = this.handleMouseUpSubmit.bind(this)

    // this.fitTheRouteInsideTheViewport = this.fitTheRouteInsideTheViewport()
    // this.handlefakeclick = this.handlefakeclick.bind(this)
    // this.getWalkingRoute = this.getWalkingRoute.bind(this)
  }

  
  handleMapClick({lngLat}) {
    this.setState({viewport: {
      longitude: lngLat[0],
      latitude: lngLat[1],
      zoom: 12,
      transitionDuration: 1000,
      transitionInterpolator: new FlyToInterpolator({
        curve: 2.4})
    }})
  }

  handleViewportChange(data) {
    this.setState({
      viewport: {
        ...this.state.viewport,
        longitude: data.center[0],
        latitude: data.center[1],
        transitionInterpolator: new LinearInterpolator(),
        transitionDuration: 1000
      }
    })
  }

  // THIS NEEDS TO RECEIVE THE DATA FROM THE GEOLOCATOR AND IF CLICKED TRIGGER THE GEOLOCATOR
  handleFindMyLocation() {
    this.setState({geolocateClick: true})
  }
// THIS NEEDS TO BE ABLE FOR A PERSON TO DROP A PIN ON THIER ORIGIN FROM BOTH THE MOUSE AND FROM MOBILE
  chooseLocationOnMap() {
    this.setState({originLonLat: [-0.071132, 51.518891]})
  }
  // handleMouseUp({lngLat, deltaTime}) {
  //   console.log(lngLat)
  //   // const lngLatString = lngLat[0].toString().substr(0,6) +'  '+ lngLat[1].toString().substr(0,6) +','+ 'Custom Location'
  //   // const originMouseUpObject = {place_name: lngLatString, center: lngLat}
  //   // const destinationMouseUpObject = {place_name: lngLatString, center: lngLat}
  //   if(deltaTime >= 300) {
  //     // this.setState({
  //     //   viewport: {
  //     //   longitude: lngLat[0],
  //     //   latitude: lngLat[1],
  //     //   zoom: 12,
  //     //   transitionDuration: 1000,
  //     //   transitionInterpolator: new LinearInterpolator({
  //     //     curve: 2.4})},
  //     // })
  //     if(this.destinationLonLat === true) {
  //       this.handleMouseUpSubmit(lngLat, 'OriginData')
  //     } else {
  //       this.handleMouseUpSubmit(lngLat, 'DestinationData')
  //     }
  //   } else {
  //     this.setState({
  //       viewport: {
  //       longitude: lngLat[0],
  //       latitude: lngLat[1],
  //       zoom: 13,
  //       transitionDuration: 1000,
  //       transitionInterpolator: new LinearInterpolator({
  //         curve: 2.4})},
  //     })
  //   }
  // }

  // handleMouseUpSubmit(lngLat, name) {
  //   const lngLatString = lngLat.toString()
  //   // if(name === 'OriginData') {
  //   //   axios.get(`api/mapbox/geocoder/${lngLatString}`)
  //   //     .then(res => this.setState({
  //   //       searchResponseData: res.data
  //   //     }))
  //   //     .then(this.displaySelectedOriginData(this.state.searchResponseData.features[0]))
  //   // } else if(name === 'DestinationData') {
  //   //   axios.get(`api/mapbox/geocoder/${lngLatString}`)
  //   //     .then(res => this.setState({
  //   //       searchResponseData: res.data
  //   //     }))
  //   //     .then(this.displaySelectedDestinationData(this.state.searchResponseData.features[0]))
  //   //   }
  //   }

  handleChange(e) {
    const target = e.target
    const value = target.value
    const name = target.name
    this.setState({ [name]: value, error: '' })
    console.log('handleChange', this.state[name])
  }

  handleSubmit(name) {
    const searchName = `is${name}SearchTriggered`
    this.setState({loadingSpinner: true, displayOriginSearchOptions: false})
    axios.get(`api/mapbox/geocoder/${this.state[name]}`)
      .then(res => this.setState({
        isSearchTriggered: true,
        [searchName]: true,
        searchResponseData: res.data
      }))
      .then(() => this.setState({loadingSpinner: false}))
      .then(console.log('submit response geocoder', this.state[name]))
      .then(console.log('geocoder search response data', this.state.searchResponseData))
  }

  handleClear(name) {
    this.setState({
      isSearchTriggered: false,
      displayBottomDestinationData: false,
      searchResponseData: searchReponseStateDefault,
      routeGeometry: routeGeometryStateDefault
    })
    const checkName = [name]
    console.log(checkName)
    const check = checkName.includes('originFormData')
    if(check == true) {
      this.setState({
        originLonLat: '',
        originFormData: '',
        originData: '',
        routePins: [],
        allParkPins: [],
        isoriginFormDataSearchTriggered: false,
  // to display "Find my location" and "Click Location on Map" set displayOriginSearchOptions to true, and do likewise under displayOriginSearchMenu()
        displayOriginSearchOptions: false
      })
    }
    else {
      this.setState({
        destinationLonLat: '',
        destinationFormData: '',
        destinationData: '',
        routePins: [],
        allParkPins: [],
        isdestinationFormDataSearchTriggered: false
      })
    }
  }

  handleDirectionsButtonClick() {
    this.setState({
      displayDirectionsSearchBar: true,
      displayDestinationSearchBar: false,
      displayOriginSearchBar: false,
      displayOriginSearchOptions: false,
      displayBottomDestinationData: false
    })
  }

  handleExploreOptionsButtonsClick(buttonName) {
    if(buttonName == 'privateButton') {
      this.setState({
        publicButton: false,
        publicPrivateButton: false,
        privateButton: true,
        parkAccessFilter: 'privateParks'
      })
    } else if(buttonName == 'publicPrivateButton') {
      this.setState({
        publicButton: false,
        publicPrivateButton: true,
        privateButton: false,
        parkAccessFilter: 'allParks'
      })
    } else {
      this.setState({
        publicButton: true,
        publicPrivateButton: false,
        privateButton: false,
        parkAccessFilter: 'publicParks'
      })
    }
  }

  handleToggleExploreClick() {
    this.setState({ toggleExplore: !this.state.toggleExplore })
    if(!this.state.toggleExplore && this.state.parkAccessFilter != 'publicParks') {
      this.setState({parkAccessFilter: 'publicParks'})}
  }

  handleOriginSearchBarArrowLeft(name) {
    this.handleClear(name)
    this.handleDirectionsButtonClick()
    this.setState({
      originLonLat: '',
      searchResponseData: searchReponseStateDefault,
      routeGeometry: routeGeometryStateDefault,
      isoriginFormDataSearchTriggered: false
    })
  }

  handleDirectionsSearchBarArrowLeft() {
    this.setState({
      displayDirectionsSearchBar: false,
      displayDestinationSearchBar: true,
      displayOriginSearchBar: false,
      displayOriginSearchOptions: false,
      displayBottomDestinationData: false,
      isRouteSelected: false,
      originLonLat: '',
      originFormData: '',
      originData: '',
      destinationData: '',
      searchResponseData: searchReponseStateDefault,
      routeGeometry: routeGeometryStateDefault,
      isoriginFormDataSearchTriggered: false,
      isdestinationFormDataSearchTriggered: false
    })
  }

  handleReverseOriginAndDestination() {
    const tempOriginLonLat = this.state.originLonLat
    const tempOriginFormData = this.state.originFormData
    const tempOriginData = this.state.originData
    this.setState({
    originLonLat: this.state.destinationLonLat,
    originFormData: this.state.destinationFormData,
    originData: this.state.destinationData,
    destinationLonLat: tempOriginLonLat,
    destinationFormData: tempOriginFormData,
    destinationData: tempOriginData,
    })
  }

  displayOriginSearchMenu() {
    this.setState({
      displayDirectionsSearchBar: false,
      displayDestinationSearchBar: false,
      displayOriginSearchBar: true,
      displayBottomDestinationData: false,
      isRouteSelected: false,
      // to display "Find my location" and "Click Location on Map" set displayOriginSearchOptions to true, likewise under HandleClear()
      displayOriginSearchOptions: false
    })
  }

  displayDestinationSearchMenu() {
    this.setState({
      displayDirectionsSearchBar: false,
      displayDestinationSearchBar: true,
      displayOriginSearchBar: false,
      displayOriginSearchOptions: false,
      displayBottomDestinationData: false,
      isRouteSelected: false
    })
  }

  displaySelectedDestinationData(data) {
    console.log('display fired', data)
    this.handleViewportChange(data)
    this.setState({
      isdestinationFormDataSearchTriggered: false,
      destinationData: data,
      destinationLonLat: data.center,
      searchResponseData: searchReponseStateDefault,
      routeGeometry: routeGeometryStateDefault
    })
    if(this.state.originFormData) {
      this.setState({
        displayBottomDestinationData: true,
        isRouteSelected: true,
        displayDirectionsSearchBar: true,
        displayDestinationSearchBar: false,
        displayOriginSearchBar: false,
        displayOriginSearchOptions: false,
      })
    } else if(!this.state.originFormData) {
      this.setState({displayBottomDestinationData: true, isRouteSelected:false})
    }
  }

  displaySelectedOriginData(data) {
    this.handleViewportChange(data)
    this.setState({
      isoriginFormDataSearchTriggered: false,
      displayOriginSearchBar: false,
      displayOriginSearchOptions: false,
      displayDirectionsSearchBar: true,
      originData: data,
      originLonLat: data.center,
      searchResponseData: searchReponseStateDefault,
      routeGeometry: routeGeometryStateDefault
    })
    // this.sendDestinationToBackend(data.center)
    console.log("origin search response data", data)
  }

  handleRecalculate() {
    this.setState({
      toggleRecalculate: !this.state.toggleRecalculate
    })
  }

  // updateParksFromExploreOptions() {
  //   axios.get(`api/parkswithinboundingbox/${this.state.originLonLat}/${this.state.destinationLonLat}/${this.state.ramblingTolerance}/${this.state.parkAccessFilter}/${this.state.sizeFormData}/${this.state.angleFilter}`)
  //   .then(res =>
  //     this.setState({
  //       allParkPins: res.data['all_waypoints_in_bbox_lon_lat']
  //   }))
  // }
  updateParksFromExploreOptions(ramblingTolerance, parkAccessFilter, sizeFormData, angleFilter) {
    axios.get(`api/parkswithinboundingbox/${this.state.originLonLat}/${this.state.destinationLonLat}/${ramblingTolerance}/${parkAccessFilter}/${sizeFormData}/${angleFilter}`)
      .then(res =>
        this.setState({
          allParkPins: res.data['all_waypoints_in_bbox_lon_lat']
        }))
  }

  sendDestinationToBackend(origin, destination) {
    console.log('mapbox request sent')
    this.setState({isMapboxSearching:true})
    axios.get(`api/parkswithinboundingbox/${origin}/${destination}/${this.state.ramblingTolerance}/${this.state.parkAccessFilter}/${this.state.sizeFormData}/${this.state.angleFilter}`)
      .then(res =>
        this.setState({
          isRouteSelected: true,
          displayBottomDestinationData: true,
          routeLargestPark: res.data['largest_park'],
          routePins: res.data['route_waypoints_lon_lat'],
          allParkPins: res.data['all_waypoints_in_bbox_lon_lat'],
          displayCommuteVsExplore: true,
          viewport: {
            ...this.state.viewport,
            longitude: res.data['midpoint'][0],
            latitude: res.data['midpoint'][1],
            zoom: 12,
            transitionInterpolator: new FlyToInterpolator({
              curve: 2.4}),
            transitionDuration: 1000
          },
          route_waypoints_lon_lat_formatted: res.data['route_waypoints_lon_lat_formatted'],
          compass_and_radius_routing_option_formatted: res.data['compass_and_radius_routing_option_formatted']
        }))
      .then(()=>this.queryBackendForRouteGeometry(this.state.route_waypoints_lon_lat_formatted, this.state.compass_and_radius_routing_option_formatted))
  }

  queryBackendForRouteGeometry(route, compassBearing) {
    axios.get(`api/queryroutegeometry/${route}/${compassBearing}`)
      .then(res =>
        this.setState({
          routeGeometry: res.data['route_geometry'],
          isMapboxSearching:false,
        }))
  }



  // sendDestinationToBackend(origin, destination, parkAccessFilter) {
  //   console.log('mapbox request sent')
  //   this.setState({isMapboxSearching:true})
  //   axios.get(`api/parkswithinboundingbox/${origin}/${destination}/${this.state.ramblingTolerance}/${this.state.parkAccessFilter}`)
  //     // .then(res =>
  //     // this.handleViewportChange(center:[res.data['center']]))
  //     .then(res =>
  //       this.setState({
  //       routeGeometry: res.data['route_geometry'],
  //       routeLargestPark: res.data['largest_park'],
  //       routePins: res.data['parks_within_perp_distance_lon_lat'],
  //       isRouteSelected: true,
  //       displayBottomDestinationData: true,
  //       viewport: {
  //         ...this.state.viewport,
  //         longitude: res.data['midpoint'][0],
  //         latitude: res.data['midpoint'][1],
  //         zoom: 12,
  //         transitionInterpolator: new FlyToInterpolator({
  //           curve: 2.4}),
  //         transitionDuration: 1000
  //       },
  //       isMapboxSearching:false
  //     }))
  //     // .then(this.fitTheRouteInsideTheViewport())
  // }

  // onClick={this.handleMouseUp}
  // onMouseDown={lnglat => this.handleMouseUp(lnglat)}
  // onClick={this.handleMapClick}
  // onMouseUp={lngLat => this.handleMouseUp({lngLat})}>

// onMouseUp={this.handleMouseUp}

  render () {
    const {viewport, originFormData, destinationFormData, originData, destinationData, displayDirectionsSearchBar, displayOriginSearchOptions, displayOriginSearchBar, displayDestinationSearchBar, displayBottomDestinationData, searchResponseData, isSearchTriggered, isdestinationFormDataSearchTriggered, isoriginFormDataSearchTriggered, routeGeometry, originLonLat, destinationLonLat, routeLargestPark, isRouteSelected, geolocateClick, loadingSpinner, isMapboxSearching, routePins, allParkPins, displayCommuteVsExplore, publicButton, publicPrivateButton, privateButton, parkAccessFilter, toggleExplore, toggleRecalculate, sizeFormData, ramblingTolerance, angleFilter} = this.state
    const directionsLayer = { routeGeometry }
    console.log(viewport)
    return (
      <div>
        <div className="mapcontainer">
          <ReactMapGl  {...viewport}
            maxTileCacheSize={10}
            height='100vh'
            width='100vw'
            mapboxApiAccessToken={process.env.MAPBOX_TOKEN}
            mapStyle="mapbox://styles/mtcolvard/ck0wmzhqq0cpu1cqo0uhf1shn"
            onViewportChange={viewport => this.setState({viewport})}
            onClick={this.handleMapClick}>
            {destinationLonLat &&
              <Pins
                originData={originData}
                destinationData={destinationData}
                parkPins={toggleExplore ? allParkPins : routePins}
              />
            }
            {routeGeometry &&
              <Source id="my-data" type="geojson" data={routeGeometry}>
                <Layer
                  type='line'
                  layout={{ 'line-cap': 'round', 'line-join': 'round' }}
                  paint={{ 'line-color': '#4790E5', 'line-width': 6 }}
                />
              </Source>
            }
            <div>
              <GeolocateControl
                style={ {position: 'absolute', bottom: 300, right: 0, margin: 10} }
                positionOptions={{enableHighAccuracy: true, timeout: 6000}}
                trackUserLocation={true}
                showAccuracyCircle={true}
                showUserLocation={true}
                captureClick={false}
                fitBoundsOption={{maxZoom: 11}}
                auto={geolocateClick}
              />
            </div>
            <div
              style={ {position: 'absolute', right: 0, bottom: 200, margin: 10} }>
              <NavigationControl
                visualizePitch={true}/>
            </div>
            <div
              style={ {position: 'absolute', bottom: 35, left: 10} }>
              <ScaleControl maxWidth={100} unit={'metric'}/>
            </div>
          </ReactMapGl>

          {originLonLat && destinationLonLat &&
            <ShouldTheRouteBeDisplayed
              originLonLat={originLonLat}
              destinationLonLat={destinationLonLat}
              toggleRecalculate={toggleRecalculate}
              sendDestinationToBackend={this.sendDestinationToBackend}/>
          }
          {toggleExplore &&
            <ShouldTheParksDisplayUpdate
              ramblingTolerance={ramblingTolerance}
              angleFilter={angleFilter}
              sizeFormData={sizeFormData}
              parkAccessFilter={parkAccessFilter}
              updateParksFromExploreOptions={this.updateParksFromExploreOptions}/>
          }
          <div className="bodyContainer">
            <div>
              <h1 className="title">FoxyMaps</h1>
            </div>
            {displayDirectionsSearchBar &&
              <SearchBarDirections
                origin={originData.place_name}
                destination={destinationData.place_name}
                onArrowLeft={this.handleDirectionsSearchBarArrowLeft}
                onReverseOriginAndDestination={this.handleReverseOriginAndDestination}
                onTriggerOriginSearchMenu={this.displayOriginSearchMenu}
                onTriggerDestinationSearchMenu={this.displayDestinationSearchMenu}
                isMapboxSearching={isMapboxSearching}/>
            }
            {displayOriginSearchBar &&
              <SearchBar
                onArrowLeft={this.handleOriginSearchBarArrowLeft}
                onDeleteField={this.handleClear}
                onHandleChange={this.handleChange}
                onHandleSubmit={this.handleSubmit}
                loadingSpinner={loadingSpinner}
                searchFormData={originFormData}
                placeholder='Enter starting point'
                name='originFormData'/>
            }
            {displayDestinationSearchBar &&
              <SearchBar
                onArrowLeft={this.handleClear}
                onDeleteField={this.handleClear}
                onHandleChange={this.handleChange}
                onHandleSubmit={this.handleSubmit}
                loadingSpinner={loadingSpinner}
                searchFormData={destinationFormData}
                placeholder='Find the scenic route to your destination'
                name='destinationFormData'/>
            }
            {originLonLat && destinationLonLat &&
              <CommuteVsExplore
                onHandleToggleClick={this.handleToggleExploreClick}
                toggleExplore={toggleExplore}/>
            }
            {displayOriginSearchOptions &&
              <div className="locationbuttonfield">
                <div className="box locationbuttonbox">
                  <button className="button is-fullwidth has-text-left" onClick={this.handleFindMyLocation}>
                    <span className="icon">
                      <FontAwesomeIcon icon="location-arrow"/></span>
                    <span>Find my location</span>
                  </button>
                  <button className="button is-fullwidth has-text-left" onClick={this.chooseLocationOnMap}>
                    <span className="icon">
                      <FontAwesomeIcon icon="map-marker-alt"/></span>
                    <span>Choose on map</span>
                  </button>
                </div>
              </div>
            }
            <div className="dropdown">
              <div>
                {isSearchTriggered && isoriginFormDataSearchTriggered && searchResponseData.features.map((element, index) =>
                  <DropDownDisplay
                    key={element.id}
                    index={index}
                    dropDownDisplayName={element.place_name}
                    searchResponseData={searchResponseData}
                    selectLocation={this.displaySelectedOriginData}
                    isSearchTriggered={isSearchTriggered}
                    name='Origin'
                  />
                )}
              </div>
            </div>
            <div className="dropdown">
              <div>
                {isSearchTriggered && isdestinationFormDataSearchTriggered && searchResponseData.features.map((element, index) =>
                  <DropDownDisplay
                    key={element.id}
                    index={index}
                    dropDownDisplayName={element.place_name}
                    searchResponseData={searchResponseData}
                    selectLocation={this.displaySelectedDestinationData}
                    isSearchTriggered={isSearchTriggered}
                    name='Destination'
                  />
                )}
              </div>
            </div>
          </div>
          {displayDirectionsSearchBar && toggleExplore && originLonLat && destinationLonLat &&
            <ExploreOptions
              onHandleExploreOptionsButtonClick={this.handleExploreOptionsButtonsClick}
              onHandleChange={this.handleChange}
              onHandleRecalculate={this.handleRecalculate}
              publicButton={publicButton}
              publicPrivateButton={publicPrivateButton}
              privateButton={privateButton}
              sizeFormData={sizeFormData}
              sizeName='sizeFormData'
              ramblingTolerance={ramblingTolerance}
              angleFilter={angleFilter}
              ramblingName='ramblingTolerance'
              angleFilterName='angleFilter'
            />}
          {displayBottomDestinationData && !toggleExplore &&
            <BottomDestinationDisplay
              onHandleDirectionsButtonClick={this.handleDirectionsButtonClick}
              destinationData={destinationData}
              routeDistance={routeGeometry['properties']['distance']}
              routeLargestPark={routeLargestPark}
              isRouteSelected={isRouteSelected}
            />
          }
        </div>
      </div>
    )
  }
}

export default Map

// fitTheRouteInsideTheViewport() {
//   const {longitude, latitude, zoom} = new WebMercatorViewport(this.state.viewport)
//     .fitBounds([this.state.originLonLat, this.state.destinationLonLat], {
//       padding: 20,
//       offset: [0, -100]
//     })
//   // const viewport = {
//   //     ...this.state.viewport,
//   //     longitude,
//   //     latitude,
//   //     zoom,
//   //     transitionDuration: 5000,
//   //     transitionInterpolator: new FlyToInterpolator(),
//   //     transitionEasing: d3.easeCubic
//   // }
//   this.setState({viewport})
// }
