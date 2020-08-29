import React from 'react'

export default class ShouldTheParksDisplayUpdate extends React.PureComponent{
  constructor(){
    super()
  }
  // componentDidMount() {
  //   console.log('componentDidMount')
  //   this.props.updateParksFromExploreOptions(this.props.sizeFormData, this.props.ramblingTolerance,  this.props.angleFilter, this.props.parkAccessFilter)
  // }
  componentDidUpdate() {
    console.log('componentDidUpdate')
    this.props.updateParksFromExploreOptions(this.props.sizeFormData, this.props.ramblingTolerance,  this.props.angleFilter, this.props.parkAccessFilter)
  }

  render() {
    return(<div></div>)
  }
}
