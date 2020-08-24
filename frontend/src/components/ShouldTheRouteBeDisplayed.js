import React from 'react'

export default class ShouldTheRouteBeDisplayed extends React.PureComponent{
  constructor(){
    super()
  }
  componentDidMount() {
    console.log('componentDidMount')
    this.props.sendDestinationToBackend(this.props.originLonLat, this.props.destinationLonLat, this.props.parkAccessFilter, this.props.toggleRecalculate)
  }
  componentDidUpdate() {
    console.log('componentDidUpdate')
    this.props.sendDestinationToBackend(this.props.originLonLat, this.props.destinationLonLat, this.props.parkAccessFilter, this.props.toggleRecalculate)
  }

  render() {
    return(<div></div>)
  }
}
