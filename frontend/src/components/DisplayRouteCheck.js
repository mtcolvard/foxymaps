import React from 'react'

class DisplayRouteCheck extends React.PureComponent{
  constructor(){
    super()
  }
  componentDidMount() {
    console.log('componentDidMount')
    this.props.sendDestinationToBackend(this.props.originLonLat, this.props.destinationLonLat)
  }
  componentDidUpdate() {
    console.log('componentDidUpdate')
    this.props.sendDestinationToBackend(this.props.originLonLat, this.props.destinationLonLat)
  }

  render() {
    return(<div></div>)
  }
}

export default DisplayRouteCheck
