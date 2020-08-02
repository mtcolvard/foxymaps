import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

export default class BottomDestinationDisplay extends React.Component {
  constructor() {
    super()
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick(e) {
    this.props.onHandleDirectionsButtonClick()
  }

  render() {
    const {isRouteSelected, routeLargestPark, destinationData, routeDistance} = this.props
    const routeDistanceFormatted = (routeDistance/1000).toFixed(2)
    const placeNameStrArray = destinationData.place_name.split(',')
    const placeName = placeNameStrArray[0]
    const placeAddress = placeNameStrArray[1]+', '+placeNameStrArray[2]
    return(
      <div className="bottomFormContainer">
        <div className="box">
          <div className="level is-mobile">
            <div className="level-left">
              <div className="level-item">
                <p className="subtitle is-5">{isRouteSelected ? 'to ' : ''}<b>{placeName}</b></p>
              </div>
            </div>
            {routeDistance &&
            <div className="level-right">
              <div className="level-item">
                <p className="subtitle is-5">{routeDistanceFormatted} km</p>
              </div>
            </div>}
          </div>
          <div className="content">
            {isRouteSelected ? <p>via {routeLargestPark}</p> : <p>{placeAddress}</p>}
            {isRouteSelected ? <div></div> :
            <button className="button is-info" onClick={this.handleClick} >
              <span className="icon">
                <FontAwesomeIcon icon="directions"/>
              </span>
              <span>Directions</span>
            </button>
          }
          </div>
        </div>
      </div>
    )
  }
}
