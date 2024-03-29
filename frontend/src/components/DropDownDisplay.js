import React from 'react'

export default class DropDownDisplay extends React.Component {
  constructor() {
    super()
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick(e) {
    this.props.selectLocation(this.props.searchResponseData.features[this.props.index])
    console.log('selectLocation', this.props.searchResponseData.features[this.props.index])
  }

  render() {
    const displayBox = this.props.isSearchTriggered
    const dropDownDisplayName = this.props.dropDownDisplayName
    return(
      <div>
        <div className="container">
          <div className={ displayBox ? 'box' : ''} onClick={this.handleClick}>
            {dropDownDisplayName}
          </div>
        </div>
      </div>
    )
  }
}
