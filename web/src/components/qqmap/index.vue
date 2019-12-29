<template>
  <div class="padd20">
    <mapselect :mapcenter="centerLatLng" :oldmarker="oldMarker" @mapclick="pointChange"></mapselect>
  </div>
</template>

<script>
import qqMapSelectPoint from "@/components/qqmap/selectPoint"
export default {
  name: "qqmap",
  components: {
    mapselect: qqMapSelectPoint
  },
  data: function() {
    return {
      pointName: "清华大学",
      qqmap: null,
      centerLatLng: "40.0024431613261,116.3263320",
      oldMarker: "40.0024431613261,116.3263320",
      newMarker: null
    };
  },
  methods: {
    pointChange(ev) {
      this.$emit("input",ev)
    }
  }
};
</script>

<style>
.qqmap {
  width: 700px;
  height: 600px;
}
</style>
