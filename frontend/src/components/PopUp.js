// import * as React from 'react'
// import {Component} from 'react'
// import {render} from 'react-dom'
// import  {
//   Popup
// } from 'react-map-gl'
//
// import ControlPanel from './control-panel'
// import Pins from './pins'
// import CityInfo from './city-info'
//
// import CITIES from '../../.data/cities.json'
//
// const geolocateStyle = {
//   position: 'absolute',
//   top: 0,
//   left: 0,
//   padding: '10px'
// }
//
// const fullscreenControlStyle = {
//   position: 'absolute',
//   top: 36,
//   left: 0,
//   padding: '10px'
// }
//
// const navStyle = {
//   position: 'absolute',
//   top: 72,
//   left: 0,
//   padding: '10px'
// }
//
// const scaleControlStyle = {
//   position: 'absolute',
//   bottom: 36,
//   left: 0,
//   padding: '10px'
// }
//
// export default class App extends Component {
//   constructor(props) {
//     super(props)
//     this.state = {
//       viewport: {
//         latitude: 37.785164,
//         longitude: -100,
//         zoom: 3.5,
//         bearing: 0,
//         pitch: 0
//       },
//       popupInfo: null
//     }
//   }
//
//   _updateViewport = viewport => {
//     this.setState({viewport})
//   }
//
//   _onClickMarker = city => {
//     this.setState({popupInfo: city})
//   }
//
//   _renderPopup() {
//     const {popupInfo} = this.state
//
//     return (
//       popupInfo && (
//         <Popup
//           tipSize={5}
//           anchor="top"
//           longitude={popupInfo.longitude}
//           latitude={popupInfo.latitude}
//           closeOnClick={false}
//           onClose={() => this.setState({popupInfo: null})}
//         >
//           <CityInfo info={popupInfo} />
//         </Popup>
//       )
//     )
//   }
//
//   render() {
//     const {viewport} = this.state
//     return (
//         <Pins data={CITIES} onClick={this._onClickMarker} />
//         {this._renderPopup()}
//     )
//   }
// }
